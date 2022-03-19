
## Step method

Each entity has a `step` method.

When inheriting, extend the `step` method instead of
simple override: Perform `super().step(queue)` calls
at the end.

The base `Entity`'s `step` method also calls
it in all children, depth first.

A `RootEntity` begins the chain of calling `step` methods.

## Action Queue

An action priority queue is passed into the `step` method.

This is done to separate calculations from impact.

During the step entities enqueue actions.
Enqueueing actions is done before `super()` calls,
thus it happens as each entity is first visited.

At the end of the step all actions are performed
in order of priorities.
In case of a tie, the actions enqueued first
are performed first.


## Action priorities

In order from high to low priority:

- PRE
- LIFETIME
  - Entity: Increase lifetime
- SPAWN
  - SpawnLocation: spawn
  - Creature: procreation
- BEGIN
- HUNGER
  - Creature: Hunger
- DISTRIBUTE
  - Resource: Distribution across those who requested
- NORMAL
- END
- MOVE 
  - EntityMovable: Movement
- DECAY
  - Creature: Max age; Starvation
  - Resource: Decay
- EXHAUSTION
  - Resource: Exhaustion
- KILL
  - EntityKillable: Death
