"""Exact mutation delta and best-retention checks against canonical simulation."""
import importlib.util
from pathlib import Path
import random
import unittest

from tools.simulate import Instance,simulate,match_count

ROOT=Path(__file__).resolve().parents[1]


def load_solver(name='anneal_cached'):
    path=ROOT/('solvers/experiments/'+name+'.py')
    if not path.exists():
        return None
    spec=importlib.util.spec_from_file_location('anneal_cached',path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AnnealTests(unittest.TestCase):
    def test_lowk_packed_rotations_and_high_action_ids(self):
        solver=load_solver('anneal_lowk_packed_beam')
        self.assertIsNotNone(solver,'retained all-action packed beam required')
        rng=random.Random(92709131)
        for n,d in ((3,2),(3,3),(10,2),(11,3),(30,2),(30,3)):
            for c in (2,6):
                a=[rng.randrange(c) for _ in range(n*n)]
                s=[rng.randrange(c) for _ in range(d*d)]
                inst=Instance(n,d,c,1,a,a[:],s)
                packed=sum(v<<(3*i) for i,v in enumerate(a+s))
                expand=solver.lowk_packed_transitions(n,d)
                children=dict(expand(packed))
                self.assertEqual(len(children),4*(n-d+1)**2)
                ids={0,1,2,3,len(children)-1}
                ids.update(rng.randrange(len(children)) for _ in range(8))
                if len(children)>256:ids.update((255,256))
                for aid in ids:
                    width=n-d+1
                    operation=(aid//4//width,aid//4%width,aid%4)
                    final,stamp=simulate(inst,[operation])
                    expected=sum(v<<(3*i) for i,v in enumerate(final+stamp))
                    self.assertEqual(children[aid],expected)
                last=len(children)-1
                self.assertEqual(dict(expand(children[last]))[last],packed)

    def test_lowk_packed_beam_two_move_oracle_and_high_id_path(self):
        solver=load_solver('anneal_lowk_packed_beam')
        self.assertIsNotNone(solver,'retained all-action packed beam required')
        rng=random.Random(92718411)
        for n,d in ((3,2),(3,3),(4,3)):
            c=3
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,2,a,t,s)
            _,_,ops,_,_=solver.build(n,d,t)
            expected=match_count(inst,a)
            for first in range(-1,len(ops)):
                for second in range(-1,len(ops)):
                    path=[ops[i] for i in (first,second) if i>=0]
                    expected=max(expected,match_count(inst,simulate(inst,path)[0]))
            found=solver.lowk_packed_beam(n,d,2,a,t,s)
            self.assertLessEqual(len(found),2)
            self.assertEqual(match_count(inst,simulate(inst,[ops[i] for i in found])[0]),expected)
            self.assertEqual(found,solver.lowk_packed_beam(n,d,2,a,t,s))
        for d in (2,3):
            n=30;a=[0]*(n*n);s=[1]*(d*d)
            op=(n-d,n-d,0)
            t,_=simulate(Instance(n,d,2,1,a,a[:],s),[op])
            path=solver.lowk_packed_beam(n,d,1,a,t,s)
            self.assertEqual(len(path),1)
            self.assertGreater(path[0],255)
            width=n-d+1
            found=[(i//4//width,i//4%width,i%4) for i in path]
            self.assertEqual(simulate(Instance(n,d,2,1,a,t,s),found)[0],t)

    def test_lowk_packed_wrapper_preserves_complete_parent(self):
        solver=load_solver('anneal_lowk_packed_beam')
        self.assertIsNotNone(solver,'retained all-action packed beam required')
        rng=random.Random(92728183)
        for n,d,c,k in ((10,2,4,4),(10,3,3,5)):
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,k,a,t,s)
            old=solver.solve_without_lowk_packed(n,d,c,k,a[:],t,s[:])
            found=solver.solve(n,d,c,k,a[:],t,s[:])
            old_score=match_count(inst,simulate(inst,old)[0])
            new_score=match_count(inst,simulate(inst,found)[0])
            self.assertGreaterEqual(new_score,old_score)
            self.assertLessEqual(len(found),k)
            if new_score==old_score:self.assertEqual(found,old)

    def test_hot_commutator_combination_preserves_hot_parent(self):
        solver=load_solver('anneal_hot_commutator_fast')
        self.assertIsNotNone(solver,'combined hot and commutator experiment required')
        rng=random.Random(92638191)
        for n,d,c,k in ((3,2,3,12),(4,3,3,24),(5,3,5,32)):
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,k,a,t,s)
            reference=solver.solve_without_commutator(n,d,c,k,a[:],t,s[:])
            found=solver.solve(n,d,c,k,a[:],t,s[:])
            old=match_count(inst,simulate(inst,reference)[0])
            new=match_count(inst,simulate(inst,found)[0])
            self.assertGreaterEqual(new,old)
            if new==old:
                self.assertEqual(found,reference)
            self.assertLessEqual(len(found),k)

    def test_retained_hot_triple_pass_is_canonical_and_deterministic(self):
        solver=load_solver('anneal_retained_hot_triple')
        self.assertIsNotNone(solver,'retained hotter triple experiment required')
        rng=random.Random(92588191)
        for _ in range(14):
            n,d,c,k=rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(3,18)
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            initial=a+s
            inst=Instance(n,d,c,k,a,t,s)
            indices,_,ops,_,_=solver.build(n,d,t)
            actions=list(zip(indices,ops))
            sequence=[rng.randrange(len(actions)) for _ in range(rng.randrange(k+1))]
            before=(initial[:],t[:],sequence[:])
            found=solver.hot_triple_repair(n,d,k,initial,t,actions,sequence,proposals=70)
            old=match_count(inst,simulate(inst,[ops[i] for i in sequence])[0])
            new=match_count(inst,simulate(inst,[ops[i] for i in found])[0])
            self.assertLessEqual(len(found),k)
            self.assertGreaterEqual(new,old)
            if new==old:
                self.assertEqual(found,sequence)
            self.assertEqual(found,solver.hot_triple_repair(n,d,k,initial,t,actions,sequence,proposals=70))
            self.assertEqual(before,(initial,t,sequence))

    def test_retained_hot_complete_wrapper_preserves_parent(self):
        solver=load_solver('anneal_retained_hot_triple')
        self.assertIsNotNone(solver,'retained hotter triple wrapper required')
        rng=random.Random(92599171)
        for n,d,c,k in ((3,2,3,9),(4,3,5,20),(5,3,6,25)):
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,k,a,t,s)
            parent=solver.solve_without_hot_restart(n,d,c,k,a[:],t,s[:])
            found=solver.solve(n,d,c,k,a[:],t,s[:])
            old=match_count(inst,simulate(inst,parent)[0])
            new=match_count(inst,simulate(inst,found)[0])
            self.assertLessEqual(len(found),k)
            self.assertGreaterEqual(new,old)
            if old==new:
                self.assertEqual(found,parent)

    def test_nested_refine_snapshots_match_canonical_and_restore_exactly(self):
        solver=load_solver('anneal_snapshot_undo')
        self.assertIsNotNone(solver,'temporary refinement snapshots required')
        rng=random.Random(214739)
        cases=[(3,2,2),(3,3,6),(30,2,6),(30,3,6)]
        cases.extend((rng.randint(4,12),rng.choice((2,3)),rng.randint(2,6)) for _ in range(12))
        for n,d,c in cases:
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            indices,_,ops,_,_=solver.build(n,d,t)
            actions=list(zip(indices,ops))
            order=list(range(len(actions)))
            rng.shuffle(order)
            state=solver.RefineState(n,d,a+s,t,actions,order)
            state.wstamp=[rng.randrange(7) for _ in range(d*d)]
            def snapshot():
                return (state.grid[:],state.stamp[:],state.wishes[:],state.wstamp[:],
                        [r[:] for r in state.values],[r[:] for r in state.goals],
                        state.counts[:] if state.counts is not None else None,
                        state.old_planes[:],state.best())
            stack=[]
            for _ in range(24):
                if stack and (len(stack)==4 or rng.randrange(3)==0):
                    undo,before=stack.pop()
                    solver.refine_restore(state,undo)
                    self.assertEqual(snapshot(),before)
                else:
                    before=snapshot()
                    aid=rng.randrange(-1,len(actions))
                    wishes=bool(rng.randrange(2))
                    grid,stamp=(state.wishes,state.wstamp) if wishes else (state.grid,state.stamp)
                    inst=Instance(n,d,6,1,grid[:],grid[:],stamp[:])
                    expected=simulate(inst,[ops[aid]] if aid>=0 else [])
                    undo=solver.refine_trial(state,aid,wishes=wishes)
                    self.assertEqual((state.wishes,state.wstamp) if wishes else
                                     (state.grid,state.stamp),expected)
                    stack.append((undo,before))
            while stack:
                undo,before=stack.pop()
                solver.refine_restore(state,undo)
                self.assertEqual(snapshot(),before)

    def test_snapshot_walkers_keep_exact_choices_and_ties(self):
        solver=load_solver('anneal_snapshot_undo')
        parent=load_solver('anneal_weighted_triple')
        self.assertIsNotNone(solver,'snapshot walker port required')
        rng=random.Random(217949)
        for name,width in (('PairWalker',2),('TripleWalker',3)):
            for _ in range(10):
                n,d,c,k=rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(3,20)
                a=[rng.randrange(c) for _ in range(n*n)]
                t=[rng.randrange(c) for _ in range(n*n)]
                s=[rng.randrange(c) for _ in range(d*d)]
                indices,_,ops,_,_=solver.build(n,d,t)
                actions=list(zip(indices,ops))
                sequence=[rng.randrange(-1,len(actions)) for _ in range(k)]
                order=list(range(len(actions)))
                rng.shuffle(order)
                old=getattr(parent,name)(n,d,a+s,t,actions,sequence,order[:])
                new=getattr(solver,name)(n,d,a+s,t,actions,sequence,order[:])
                for _ in range(20):
                    position=rng.randrange(k-width+1)
                    old.move(position)
                    new.move(position)
                    side=rng.randrange(2)
                    if width==3:
                        self.assertEqual(new.informed(side),old.informed(side))
                    args=(rng.randrange(-1,len(actions)),side if width==2 else rng.randrange(-1,len(actions)))
                    expected=old.propose(*args)
                    found=new.propose(*args)
                    self.assertEqual(found,expected)
                    old.accept(*expected)
                    new.accept(*found)
                    self.assertEqual((new.sequence,new.score,new.state.best()),
                                     (old.sequence,old.score,old.state.best()))

    def test_informed_triple_endpoints_are_exact_and_restore_boundary(self):
        solver=load_solver('anneal_weighted_triple')
        self.assertIsNotNone(solver,'informed triple walker required')
        rng=random.Random(914271)
        for _ in range(8):
            n,d,c,k=rng.randint(3,6),rng.choice((2,3)),rng.randint(2,6),rng.randint(3,12)
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,k,a,t,s)
            indices,_,ops,_,_=solver.build(n,d,t)
            actions=list(zip(indices,ops))
            ids=[rng.randrange(-1,len(actions)) for _ in range(k)]
            order=list(range(len(actions)))
            rng.shuffle(order)
            walker=solver.TripleWalker(n,d,a+s,t,actions,ids,order)
            for _ in range(4):
                p=rng.randrange(k-2)
                walker.move(p)
                for side in range(2):
                    state=walker.state
                    before=(state.grid[:],state.stamp[:],state.wishes[:],state.wstamp[:],state.best(),walker.boundary_score)
                    fixed=walker.informed(side)
                    self.assertEqual(before,(state.grid,state.stamp,state.wishes,state.wstamp,state.best(),walker.boundary_score))
                    def score(aid):
                        sequence=walker.sequence[:]
                        sequence[p+1]=-1
                        sequence[p+2*side]=aid
                        return match_count(inst,simulate(inst,[ops[i] for i in sequence if i>=0])[0])
                    self.assertEqual(score(fixed),max(score(aid) for aid in range(-1,len(actions))))

    def test_informed_triple_layer_preserves_weighted_parent(self):
        solver=load_solver('anneal_weighted_triple')
        parent=load_solver('forward_weighted_refine_informed')
        self.assertIsNotNone(solver,'informed triple merge required')
        rng=random.Random(794139)
        for n,d,c,k in ((3,2,3,7),(4,3,2,5),(5,3,6,16),(7,2,4,28),(9,3,5,45)):
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,k,a,t,s)
            old=parent.solve(n,d,c,k,a[:],t,s[:])
            found=solver.solve(n,d,c,k,a[:],t,s[:])
            self.assertLessEqual(len(found),k)
            self.assertGreaterEqual(match_count(inst,simulate(inst,found)[0]),
                                    match_count(inst,simulate(inst,old)[0]))

    def test_cached_window_scores_match_canonical_and_old_proposals(self):
        solver=load_solver('anneal_fast_walkers')
        parent=load_solver('anneal_triple_cached')
        self.assertIsNotNone(solver,'cached boundary walkers required')
        rng=random.Random(213719)
        for name,width in (('PairWalker',2),('TripleWalker',3)):
            for _ in range(16):
                n,d,c,k=rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(3,18)
                a=[rng.randrange(c) for _ in range(n*n)]
                t=[rng.randrange(c) for _ in range(n*n)]
                s=[rng.randrange(c) for _ in range(d*d)]
                inst=Instance(n,d,c,k,a,t,s)
                indices,_,ops,_,_=solver.build(n,d,t)
                actions=list(zip(indices,ops))
                ids=[rng.randrange(-1,len(actions)) for _ in range(k)]
                order=list(range(len(actions)))
                rng.shuffle(order)
                old=getattr(parent,name)(n,d,a+s,t,actions,ids,order[:])
                found=getattr(solver,name)(n,d,a+s,t,actions,ids,order[:])
                for _ in range(20):
                    position=rng.randrange(k-width+1)
                    old.move(position)
                    found.move(position)
                    if width==2:
                        args=rng.randrange(-1,len(actions)),rng.randrange(2)
                    else:
                        args=rng.randrange(-1,len(actions)),rng.randrange(-1,len(actions))
                    expected=old.propose(*args)
                    actual=found.propose(*args)
                    self.assertEqual(actual,expected)
                    state=found.state
                    self.assertEqual(found.boundary_score,sum(x==y for x,y in
                        zip(state.grid+state.stamp,state.wishes+state.wstamp)))
                    old.accept(*expected)
                    found.accept(*actual)
                    canonical=simulate(inst,[ops[i] for i in found.sequence if i>=0])
                    self.assertEqual(found.score,match_count(inst,canonical[0]))

    def test_hot_restart_retains_best_and_is_deterministic(self):
        solver=load_solver('anneal_hot_restart_cached')
        self.assertIsNotNone(solver,'hot restart implementation required')
        rng=random.Random(714989)
        for _ in range(10):
            n,d,c,k=rng.randint(3,7),rng.choice((2,3)),rng.randint(2,6),rng.randint(3,15)
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,k,a,t,s)
            indices,_,ops,_,_=solver.build(n,d,t)
            actions=list(zip(indices,ops))
            ids=[rng.randrange(len(actions)) for _ in range(k)]
            old=match_count(inst,simulate(inst,[ops[j] for j in ids])[0])
            found=solver.anneal_hot(n,d,k,a+s,t,actions,ids,proposals=100)
            self.assertGreaterEqual(match_count(inst,simulate(inst,[ops[j] for j in found])[0]),old)
            self.assertLessEqual(len(found),k)
            self.assertEqual(found,solver.anneal_hot(n,d,k,a+s,t,actions,ids,proposals=100))

    def test_dual_small_merge_preserves_short_annealing(self):
        solver=load_solver('anneal_retained_dual_sa')
        parent=load_solver('anneal_guided_walk_sa_short')
        self.assertIsNotNone(solver,'dual small-board annealing merge required')
        rng=random.Random(413789)
        for n,d,c,k in ((4,2,3,12),(5,3,6,25),(6,2,4,35),(8,3,6,17)):
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,k,a,t,s)
            old=parent.solve(n,d,c,k,a[:],t,s[:])
            found=solver.solve(n,d,c,k,a[:],t,s[:])
            self.assertGreaterEqual(match_count(inst,simulate(inst,found)[0]),
                                    match_count(inst,simulate(inst,old)[0]))

    def test_triple_walker_moves_and_proposals_match_canonical(self):
        solver=load_solver('anneal_triple_walk')
        self.assertIsNotNone(solver,'triple walker implementation required')
        rng=random.Random(741271)
        for _ in range(12):
            n,d,c,k=rng.randint(3,7),rng.choice((2,3)),rng.randint(2,6),rng.randint(4,16)
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,k,a,t,s)
            indices,_,ops,_,_=solver.build(n,d,t)
            actions=list(zip(indices,ops))
            ids=[rng.randrange(-1,len(actions)) for _ in range(k)]
            walker=solver.TripleWalker(n,d,a+s,t,actions,ids,list(range(len(actions))))
            for _ in range(20):
                walker.move(rng.randrange(k-2))
                p=walker.position
                prefix=simulate(inst,[ops[i] for i in walker.sequence[:p] if i>=0])
                self.assertEqual(walker.state.grid+walker.state.stamp,prefix[0]+prefix[1])
                desired=Instance(n,d,6,k,t,t,[6]*(d*d))
                suffix=[ops[i] for i in reversed(walker.sequence[p+3:]) if i>=0]
                wishes=simulate(desired,suffix)
                self.assertEqual(walker.state.wishes+walker.state.wstamp,wishes[0]+wishes[1])
                ends=[rng.randrange(-1,len(actions)) for _ in range(2)]
                proposal,delta=walker.propose(*ends)
                candidate=walker.sequence[:]
                candidate[p:p+3]=proposal
                expected=match_count(inst,simulate(inst,[ops[i] for i in candidate if i>=0])[0])
                self.assertEqual(walker.score+delta,expected)
                walker.accept(proposal,delta)
                self.assertEqual(walker.score,expected)

    def test_triple_walk_annealing_retains_best(self):
        solver=load_solver('anneal_triple_walk')
        self.assertIsNotNone(solver,'triple annealing implementation required')
        rng=random.Random(217417)
        for _ in range(12):
            n,d,c,k=rng.randint(3,7),rng.choice((2,3)),rng.randint(2,6),rng.randint(3,16)
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,k,a,t,s)
            indices,_,ops,_,_=solver.build(n,d,t)
            actions=list(zip(indices,ops))
            ids=[rng.randrange(len(actions)) for _ in range(k)]
            old=match_count(inst,simulate(inst,[ops[j] for j in ids])[0])
            found=solver.anneal_triples(n,d,k,a+s,t,actions,ids,proposals=80)
            self.assertGreaterEqual(match_count(inst,simulate(inst,[ops[j] for j in found])[0]),old)
            self.assertLessEqual(len(found),k)
            self.assertEqual(found,solver.anneal_triples(n,d,k,a+s,t,actions,ids,proposals=80))

    def test_retained_small_merge_preserves_parent_score(self):
        solver=load_solver('anneal_retained_small_sa')
        self.assertIsNotNone(solver,'retained small-board annealing merge required')
        rng=random.Random(792137)
        for n,d,c,k in ((3,2,2,1),(3,3,3,2),(4,2,6,9),
                        (5,3,4,25),(6,2,3,30),(7,3,6,12)):
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,k,a,t,s)
            old=solver.solve_before_pair_annealing(n,d,c,k,a[:],t,s[:])
            found=solver.solve(n,d,c,k,a[:],t,s[:])
            self.assertLessEqual(len(found),k)
            self.assertGreaterEqual(match_count(inst,simulate(inst,found)[0]),
                                    match_count(inst,simulate(inst,old)[0]))

    def test_annealing_skips_search_at_inventory_bound(self):
        solver=load_solver('anneal_retained_small_sa')
        n,d,k=3,2,20
        grid=[0]*9
        stamp=[1]*4
        target=[1]*9
        indices,_,ops,_,_=solver.build(n,d,target)
        actions=list(zip(indices,ops))
        sequence=[0]
        def unexpected_search(*args,**kwargs):
            self.fail('a sequence at the inventory upper bound needs no search')
        solver.PairWalker=unexpected_search
        found=solver.anneal_walk(n,d,k,grid+stamp,target,actions,sequence)
        inst=Instance(n,d,2,k,grid,target,stamp)
        self.assertEqual(match_count(inst,simulate(inst,[ops[i] for i in found])[0]),4)

    def test_pair_walk_annealing_retains_best_and_is_deterministic(self):
        solver=load_solver('anneal_pair_walk_sa')
        self.assertIsNotNone(solver,'pair-walk annealing implementation required')
        rng=random.Random(1479817)
        for _ in range(16):
            n,d,c,k=rng.randint(3,7),rng.choice((2,3)),rng.randint(2,6),rng.randint(3,16)
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,k,a,t,s)
            indices,_,ops,_,_=solver.build(n,d,t)
            actions=list(zip(indices,ops))
            ids=[rng.randrange(len(actions)) for _ in range(k)]
            old=match_count(inst,simulate(inst,[ops[j] for j in ids])[0])
            found=solver.anneal_walk(n,d,k,a+s,t,actions,ids,proposals=160)
            self.assertGreaterEqual(match_count(inst,simulate(inst,[ops[j] for j in found])[0]),old)
            self.assertLessEqual(len(found),k)
            self.assertEqual(found,solver.anneal_walk(n,d,k,a+s,t,actions,ids,proposals=160))

    def test_pair_walker_moves_and_mutations_match_canonical(self):
        solver=load_solver('anneal_pair_walk')
        self.assertIsNotNone(solver,'pair-walking implementation required')
        rng=random.Random(191917)
        for _ in range(18):
            n,d,c,k=rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(3,20)
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,k,a,t,s)
            indices,_,ops,_,_=solver.build(n,d,t)
            actions=list(zip(indices,ops))
            ids=[rng.randrange(-1,len(actions)) for _ in range(k)]
            order=list(range(len(actions)))
            rng.shuffle(order)
            walker=solver.PairWalker(n,d,a+s,t,actions,ids,order)
            for _ in range(25):
                walker.move(rng.randrange(k-1))
                p=walker.position
                prefix=simulate(inst,[ops[i] for i in walker.sequence[:p] if i>=0])
                self.assertEqual(walker.state.grid+walker.state.stamp,prefix[0]+prefix[1])
                desired=Instance(n,d,6,k,t,t,[6]*(d*d))
                suffix=[ops[i] for i in reversed(walker.sequence[p+2:]) if i>=0]
                wishes=simulate(desired,suffix)
                self.assertEqual(walker.state.wishes+walker.state.wstamp,wishes[0]+wishes[1])
                pair,delta=walker.propose(rng.randrange(-1,len(actions)),rng.randrange(2))
                candidate=walker.sequence[:]
                candidate[p:p+2]=pair
                expected=match_count(inst,simulate(inst,[ops[i] for i in candidate if i>=0])[0])
                self.assertEqual(walker.score+delta,expected)
                walker.accept(pair,delta)
                self.assertEqual(walker.score,expected)

    def test_beam_triple_merge_preserves_parent(self):
        solver=load_solver('anneal_beam_guided')
        rng=random.Random(7433341)
        for _ in range(12):
            n,d,c,k=rng.randint(3,6),rng.choice((2,3)),rng.randint(2,6),rng.randint(1,20)
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,k,a,t,s)
            old=solver.construct_all(n,d,c,k,a[:],t,s[:])
            found=solver.solve(n,d,c,k,a[:],t,s[:])
            self.assertGreaterEqual(match_count(inst,simulate(inst,found)[0]),
                                    match_count(inst,simulate(inst,old)[0]))

    def test_triple_completion_is_exact_and_restores_state(self):
        solver=load_solver('anneal_triple')
        self.assertIsNotNone(solver,'triple completion implementation required')
        rng=random.Random(1941401)
        for _ in range(20):
            n,d,c=rng.randint(3,6),rng.choice((2,3)),rng.randint(2,6)
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,180,a,t,s)
            indices,_,ops,_,_=solver.build(n,d,t)
            actions=list(zip(indices,ops))
            order=list(range(len(actions)))
            rng.shuffle(order)
            state=solver.RefineState(n,d,a+s,t,actions,order)
            for _ in range(5):
                state.apply(rng.randrange(len(actions)),wishes=True)
            wanted=state.wishes+state.wstamp
            before=(state.grid[:],state.stamp[:],wanted[:],state.best())
            original=[rng.randrange(-1,len(actions)) for _ in range(3)]
            left=[rng.randrange(-1,len(actions)) for _ in range(4)]
            right=[rng.randrange(-1,len(actions)) for _ in range(4)]
            found=solver.optimize_triple(state,*original,left,right)
            def score(triple):
                final,stamp=simulate(inst,[ops[i] for i in triple if i>=0])
                return sum(x==y for x,y in zip(final+stamp,wanted))
            best=score(original)
            for first in left:
                for last in right:
                    for middle in range(-1,len(actions)):
                        best=max(best,score((first,middle,last)))
            self.assertEqual(score(found),best)
            self.assertEqual(before,(state.grid,state.stamp,state.wishes+state.wstamp,state.best()))

    def test_direct_low_budget_search_matches_all_legal_sequences(self):
        solver=load_solver('anneal_pair_exact')
        rng=random.Random(901441)
        for _ in range(12):
            n,d,c,k=rng.randint(3,5),rng.choice((2,3)),rng.randint(2,6),rng.choice((1,2))
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,k,a,t,s)
            indices,_,ops,_,_=solver.build(n,d,t)
            actions=list(zip(indices,ops))
            found=solver.exact_low_budget(n,d,k,a+s,t,actions)
            actual=match_count(inst,simulate(inst,[ops[i] for i in found])[0])
            best=0
            for first in range(-1,len(actions)):
                for second in range(-1,len(actions)) if k==2 else (-1,):
                    pair=[ops[i] for i in (first,second) if i>=0]
                    best=max(best,match_count(inst,simulate(inst,pair)[0]))
            self.assertEqual(actual,best)

    def test_two_operation_exhaustive_search_is_globally_optimal(self):
        solver=load_solver('anneal_pair_exhaustive')
        rng=random.Random(1743341)
        for _ in range(10):
            n,d,c=rng.randint(3,5),rng.choice((2,3)),rng.randint(2,6)
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,2,a,t,s)
            indices,_,ops,_,_=solver.build(n,d,t)
            actions=list(zip(indices,ops))
            found=solver.pair_sweep(n,d,2,a+s,t,actions,[0,0])
            actual=match_count(inst,simulate(inst,[ops[i] for i in found])[0])
            best=0
            for first in range(-1,len(actions)):
                for second in range(-1,len(actions)):
                    pair=[ops[i] for i in (first,second) if i>=0]
                    best=max(best,match_count(inst,simulate(inst,pair)[0]))
            self.assertEqual(actual,best)

    def test_incremental_pair_choice_matches_exhaustive_completion(self):
        solver=load_solver('anneal_pair_sweep')
        rng=random.Random(171741)
        for _ in range(18):
            n,d,c=rng.randint(3,6),rng.choice((2,3)),rng.randint(2,6)
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,180,a,t,s)
            indices,_,ops,_,_=solver.build(n,d,t)
            actions=list(zip(indices,ops))
            order=list(range(len(actions)))
            rng.shuffle(order)
            state=solver.RefineState(n,d,a+s,t,actions,order)
            for _ in range(5):
                state.apply(rng.randrange(len(actions)),wishes=True)
            wanted=state.wishes+state.wstamp
            before=(state.grid[:],state.stamp[:],wanted[:],state.best())
            first,second=[rng.randrange(-1,len(actions)) for _ in range(2)]
            candidates=[(rng.randrange(-1,len(actions)),rng.randrange(2)) for _ in range(8)]
            found=solver.optimize_pair(state,first,second,candidates)
            def score(pair):
                final,stamp=simulate(inst,[ops[i] for i in pair if i>=0])
                return sum(x==y for x,y in zip(final+stamp,wanted))
            best=max(score((first,second)),score((-1,-1)))
            for fixed,side in candidates:
                for other in range(-1,len(actions)):
                    best=max(best,score((other,fixed) if side else (fixed,other)))
            self.assertEqual(score(found),best)
            self.assertEqual(before,(state.grid,state.stamp,state.wishes+state.wstamp,state.best()))

    def test_pair_sweeps_preserve_sequence_score(self):
        solver=load_solver('anneal_pair_sweep')
        self.assertIsNotNone(solver,'incremental pair sweep implementation required')
        rng=random.Random(815179)
        for _ in range(32):
            n,d,c,k=rng.randint(3,9),rng.choice((2,3)),rng.randint(2,6),rng.randint(1,25)
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,k,a,t,s)
            indices,_,ops,_,_=solver.build(n,d,t)
            actions=list(zip(indices,ops))
            ids=[rng.randrange(len(actions)) for _ in range(k)]
            old=match_count(inst,simulate(inst,[ops[j] for j in ids])[0])
            found=solver.pair_sweep(n,d,k,a+s,t,actions,ids,passes=2,width=8)
            new=match_count(inst,simulate(inst,[ops[j] for j in found])[0])
            self.assertGreaterEqual(new,old)
            self.assertLessEqual(len(found),k)

    def test_pair_repair_never_loses_score(self):
        solver=load_solver('anneal_pair')
        self.assertIsNotNone(solver,'pair repair implementation required')
        rng=random.Random(981423)
        for _ in range(20):
            n,d,c,k=rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(2,20)
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,k,a,t,s)
            indices,_,ops,_,_=solver.build(n,d,t)
            actions=list(zip(indices,ops))
            ids=[rng.randrange(len(actions)) for _ in range(k)]
            old=match_count(inst,simulate(inst,[ops[j] for j in ids])[0])
            found=solver.pair_repair(n,d,k,a+s,t,actions,ids,proposals=40)
            new=match_count(inst,simulate(inst,[ops[j] for j in found])[0])
            self.assertGreaterEqual(new,old)
            self.assertLessEqual(len(found),k)

    def test_mutations_match_full_simulation(self):
        solver=load_solver()
        self.assertIsNotNone(solver,'annealing solver implementation required')
        rng=random.Random(143313)
        for _ in range(40):
            n,d,c,k=rng.randint(3,9),rng.choice((2,3)),rng.randint(2,6),rng.randint(3,30)
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,k,a,t,s)
            indices,_,ops,_,_=solver.build(n,d,t)
            actions=list(zip(indices,ops))
            ids=[rng.randrange(-1,len(actions)) for _ in range(k)]
            state=solver.SequenceState(a+s,t,actions,ids,n*n)
            for mutation in range(30):
                i=rng.randrange(k-1)
                replacements=[rng.randrange(-1,len(actions))]
                if mutation%2:
                    replacements.append(rng.randrange(-1,len(actions)))
                candidate=state.sequence[:]
                candidate[i:i+len(replacements)]=replacements
                result=simulate(inst,[ops[j] for j in candidate if j>=0])
                expected=match_count(inst,result[0])
                delta=state.delta(i,replacements)
                self.assertEqual(state.score+delta,expected)
                state.accept(i,replacements,delta)
                self.assertEqual(state.score,expected)
                self.assertEqual(state.prefix[-1],result[0]+result[1])
                self.assertEqual(state.score,sum(x==y for x,y in zip(a+s,state.wishes[0])))

    def test_annealing_retains_best_valid_sequence(self):
        solver=load_solver()
        self.assertIsNotNone(solver,'annealing solver implementation required')
        rng=random.Random(149133)
        for _ in range(20):
            n,d,c,k=rng.randint(3,8),rng.choice((2,3)),rng.randint(2,6),rng.randint(2,20)
            a=[rng.randrange(c) for _ in range(n*n)]
            t=[rng.randrange(c) for _ in range(n*n)]
            s=[rng.randrange(c) for _ in range(d*d)]
            inst=Instance(n,d,c,k,a,t,s)
            indices,_,ops,_,_=solver.build(n,d,t)
            actions=list(zip(indices,ops))
            ids=[rng.randrange(len(actions)) for _ in range(k)]
            old=match_count(inst,simulate(inst,[ops[j] for j in ids])[0])
            found=solver.anneal(n,d,k,a+s,t,actions,ids,proposals=200)
            new=match_count(inst,simulate(inst,[ops[j] for j in found])[0])
            self.assertGreaterEqual(new,old)
            self.assertLessEqual(len(found),k)
            self.assertEqual(found,solver.anneal(n,d,k,a+s,t,actions,ids,proposals=200))


if __name__=='__main__':
    unittest.main()
