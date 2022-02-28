
### Step events

Each entity has 3 step "events", in order of execution:

- Begin step
- Step
- End step

The same event will be run among all child sentities, depth first.

### What is done during each event

- Begin step
  - Entity: incrementing lifetime
  - SpawnerLocation: spawning
- Step
  - Main logic of entities
- End step
  - Creature: Checking against max_lifetime
  - Resource: Checking against threshold
  - Movable: Movement of entities
  - Killable: Killing entities set as killed
