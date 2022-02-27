
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
  - Movable: Movement of entities
  - Killable: Checking against max_lifetime
  - Killable: Killing entities set as killed
