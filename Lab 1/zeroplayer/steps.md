
### Step events overview

Each entity has 3 step "events", in order of execution:

- Begin step
- Step
- End step

The same event will be run among  all entities,
starting with the root entity and continuing
depth first, executing event on the way down.

This was done to separate calculation of actions
affecting other entities
from performing them.

\*_children step events exist because of
inheritance and super() calls.

### Event contents

- Begin step
  - Entity: incrementing lifetime
  - SpawnerLocation: spawning
  - Resource: Decay
  - Creature: Hunger
  - Creature: Eating logic
- Step
  - Main logic of entities
- End step
  - Creature: Checking against max_lifetime
  - Creature: Starving check
  - Resource: Checking against threshold
  - Movable: Movement of entities
  - Killable: Killing entities set as killed
