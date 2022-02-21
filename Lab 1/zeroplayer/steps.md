
### Step events

Each entity has 3 step "events", in order of execution:

- Begin step
- Step
- End step

The same event will be run among all entities, depth first.

### What is done during each event

- Begin step
  - Incrementing lifetime
  - Spawning children
- Step
  - ...
- End step
  - ...