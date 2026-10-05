"""Independent scalar/boundary oracles for the planes-only RefineState port."""
import copy
import random
import unittest

from solvers.experiments import refine_planes_only as candidate
from solvers.experiments import late_beam_four_fast as reference


class RefinePlanesReviewTests(unittest.TestCase):
    def state(self, n, d, initial, target, rng):
        indices, _, operations, _, _ = candidate.build(n,d,target)
        actions = list(zip(indices,operations))
        order = list(range(len(actions)))
        rng.shuffle(order)
        return candidate.RefineState(n,d,initial,target,actions,order)

    def assert_planes(self,state):
        self.assertIsNone(state.counts)
        for aid,(patch,_) in enumerate(state.actions):
            expected = state.dd-sum(state.grid[p]==state.wishes[p] for p in patch)
            actual = sum(((bits>>aid)&1)<<plane
                         for plane,bits in enumerate(state.old_planes))
            self.assertEqual(actual,expected,(aid,actual,expected))
        for plane in state.old_planes:
            self.assertEqual(plane & ~state.all_bits,0)
        self.assertEqual(state.old_planes[4],0)

    def assert_scalar_best(self,state):
        best,chosen = -1000,-1
        for aid in state.order:
            gain = sum((state.stamp[j]==state.wishes[p])
                       +(state.grid[p]==state.wstamp[j])
                       -(state.grid[p]==state.wishes[p])
                       -(state.stamp[j]==state.wstamp[j])
                       for j,p in enumerate(state.actions[aid][0]))
            if gain>best:
                best,chosen=gain,aid
        expected = (-1,0) if best<0 else (chosen,best)
        self.assertEqual(state.best(),expected)

    def test_extreme_match_counts_and_wildcard_borrow_carry(self):
        rng=random.Random(2026092581)
        for n,d in ((3,2),(3,3),(4,3),(7,2),(7,3),(30,2),(30,3)):
            for mode in range(3):
                target=[0]*(n*n)
                grid=[int(mode==1)]*(n*n)
                if mode==2:
                    grid=[rng.randrange(2) for _ in grid]
                    target=[rng.randrange(2) for _ in grid]
                state=self.state(n,d,grid+[1]*(d*d),target,rng)
                self.assert_planes(state)
                for step in range(8):
                    region=(0,len(state.regions)-1,len(state.regions)//2)[step%3]
                    state.apply(4*region+step%4,wishes=bool(step%2))
                    self.assert_planes(state)
                    if n<=7:self.assert_scalar_best(state)

    def test_nested_restore_keeps_none_and_exact_boundary_state(self):
        rng=random.Random(2026092582)
        fields=('grid','stamp','wishes','wstamp','values','goals','old_planes')
        for n,d in ((3,3),(6,2),(8,3),(30,3)):
            initial=[rng.randrange(6) for _ in range(n*n+d*d)]
            target=[rng.randrange(6) for _ in range(n*n)]
            state=self.state(n,d,initial,target,rng)
            stack=[]
            for side in (False,True,False,True):
                before={key:copy.deepcopy(getattr(state,key)) for key in fields}
                undo=candidate.refine_trial(state,rng.randrange(len(state.actions)),side)
                stack.append((before,undo))
                self.assert_planes(state)
            while stack:
                before,undo=stack.pop()
                candidate.refine_restore(state,undo)
                self.assertIsNone(state.counts)
                for key,value in before.items():self.assertEqual(getattr(state,key),value)
                self.assert_planes(state)
            self.assertIsNone(candidate.refine_trial(state,-1))
            candidate.refine_restore(state,None)
            self.assert_planes(state)

    def test_weighted_cache_warmup_in_both_orders(self):
        rng=random.Random(2026092583)
        fields=('grid','stamp','wishes','wstamp','weights','wstamp_weights',
                'values','goals','weight_bits','counts','old_planes')
        for n,d in ((3,2),(4,3),(9,3),(16,2)):
            for weighted_first in (False,True):
                candidate._REFINE_GEOMETRY.clear()
                candidate._REFINE_COVER_BITS.clear()
                initial=[rng.randrange(6) for _ in range(n*n+d*d)]
                target=[rng.randrange(6) for _ in range(n*n)]
                weights=[rng.randrange(3) for _ in target]
                indices,_,operations,_,_=candidate.build(n,d,target)
                actions=list(zip(indices,operations));order=list(range(len(actions)))
                rng.shuffle(order)
                if not weighted_first:
                    candidate.RefineState(n,d,initial,target,actions,order)
                before=reference.WeightedRefineState(n,d,initial,target,weights,actions,order)
                after=candidate.WeightedRefineState(n,d,initial,target,weights,actions,order)
                plain=candidate.RefineState(n,d,initial,target,actions,order)
                self.assert_planes(plain)
                for p,mask in enumerate(plain.cover_bits):
                    expected=0
                    for aid,(patch,_) in enumerate(actions):
                        if p in patch:expected|=1<<aid
                    self.assertEqual(mask,expected)
                for _ in range(12):
                    aid,side=rng.randrange(len(actions)),bool(rng.randrange(2))
                    before.apply(aid,side);after.apply(aid,side)
                    for field in fields:self.assertEqual(getattr(before,field),getattr(after,field))
                    self.assertEqual(before.best(),after.best())
                    self.assertIsInstance(after.counts,list)


if __name__ == '__main__':
    unittest.main()
