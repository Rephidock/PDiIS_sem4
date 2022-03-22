from typing import Optional, Callable, Type
import keyboard
import animals_sim
from zeroplayer.entities.entity import Entity
from zeroplayer.entities.entity import RootEntity

from zeroplayer.display_chunk import DisplayChunk
from utils.string_utils import str_proxy
import utils.activator as activator


class Lab1:

    #region //// Init, Main

    def __init__(self):
        self.__init_sim()
        self.___init_controls()
        self.__init_interference()

    def main(self):

        # Initial drawing
        self.draw()

        while True:
            do_exit = self.handle_key_event(keyboard.read_event())
            if do_exit:
                break

    #endregion

    #region //// Drawing

    display_header: str = "-= PDiIS Lab 1 - Step simulation =-"

    @staticmethod
    def draw_clear() -> None:
        print("\033[2J\033[H", end="")

    def draw(self) -> None:
        self.draw_clear()

        # Header
        print(self.display_header)

        # Simulation
        print("\n\n", end="")

        if self.sim_root is None:
            print("[ No simulation active ]")
        else:
            print(
                DisplayChunk.from_entity(
                    self.sim_root,
                    overrides=animals_sim.display.overrides,
                    force_chunk_types=animals_sim.display.forced_chunks
                )
            )

        print("\n\n", end="")

        if self.is_interfering:
            # Interference
            self.draw_interference()
        else:
            # Controls
            print(self.display_controls)

    #endregion

    #region //// Controls

    forward_rules: dict[int, Callable[[], None | bool]]
    display_controls: str = "[O] - Open. [S] - Save. [N] - New.\n[Space] - Step single. [I] - Interfer [ESC] - Exit."

    def ___init_controls(self) -> None:
        self.forward_rules = {
            keyboard.key_to_scan_codes("esc")[0]: lambda: True,
            keyboard.key_to_scan_codes("f5")[0]: self.draw,
            keyboard.key_to_scan_codes("o")[0]: self.sim_open,
            keyboard.key_to_scan_codes("s")[0]: self.sim_save,
            keyboard.key_to_scan_codes("n")[0]: self.sim_new,
            keyboard.key_to_scan_codes("i")[0]: self.sim_interfere,
            keyboard.key_to_scan_codes("space")[0]: self.sim_step
        }

    def handle_key_event(self, event: keyboard.KeyboardEvent) -> bool:
        """
        Returns True if user exited the app.
        """

        # Only check for presses, not releases
        if event.event_type == keyboard.KEY_UP:
            return False

        # Interference (special case)
        if self.is_interfering:
            self.sim_interfere(event.scan_code)
            return False

        # Find method
        lookup = self.forward_rules.get(event.scan_code)
        if lookup is None:
            return False

        # Call and return
        ret = lookup()
        return bool(ret)  # None will become False

    #endregion

    #region //// Simulation and interaction

    sim_root: Optional[RootEntity]

    def __init_sim(self):
        self.sim_root = None

    def sim_new(self):
        self.sim_root = animals_sim.create.create_new()
        self.draw()

    def sim_step(self):
        if self.sim_root is not None:
            self.sim_root.root_step()
            self.draw()

    def sim_save(self):
        raise NotImplementedError

    def sim_open(self):
        raise NotImplementedError

    #endregion

    #region //// Interference

    is_interfering: bool
    is_spawning: bool

    interference_keycode_to_index: dict[int, int] = {
        keyboard.key_to_scan_codes("0")[0]: 0,
        keyboard.key_to_scan_codes("1")[0]: 1,
        keyboard.key_to_scan_codes("2")[0]: 2,
        keyboard.key_to_scan_codes("3")[0]: 3,
        keyboard.key_to_scan_codes("4")[0]: 4,
        keyboard.key_to_scan_codes("5")[0]: 5,
        keyboard.key_to_scan_codes("6")[0]: 6,
        keyboard.key_to_scan_codes("7")[0]: 7,
        keyboard.key_to_scan_codes("8")[0]: 8,
        keyboard.key_to_scan_codes("9")[0]: 9
    }

    interference_spawn_options: list[Type[Entity]] = [
        animals_sim.entities.herbivores.Mouse,
        animals_sim.entities.herbivores.Rabbit,
        animals_sim.entities.predators.Owl,
        animals_sim.entities.predators.Fox
    ]

    interference_location_choices: list[int]  # menu id -> entity id
    interference_location: Optional[Entity]

    interference_controls: str = "[ESC] - Back. [0..9] - Confirm option."
    interference_prompt_location: str = "Select location:"
    interference_prompt_entity: str = "Select creature:"

    def __init_interference(self):
        self.is_interfering = False
        self.is_spawning = False
        self.interference_location_choices = list()
        self.interference_location = None

    def draw_interference(self):
        if not self.is_interfering:
            return

        print(self.interference_controls, end="")
        print("\n\n", end="")

        if not self.is_spawning:
            # Location
            print(self.interference_prompt_location)
            for i, entity_id in enumerate(self.interference_location_choices):
                entity_str = str_proxy(self.sim_root.children[entity_id], overrides=animals_sim.display.overrides)
                print(f"[{i}] - {entity_str}")
            return

        # Creature
        print(f"Location: {str_proxy(self.interference_location, overrides=animals_sim.display.overrides)}")
        print(self.interference_prompt_entity)
        for i, entity_type in enumerate(self.interference_spawn_options):
            print(f"[{i}] - {entity_type.__name__}")
        return

    def sim_interfere(self, keycode: Optional[int] = None):
        if self.sim_root is None:
            return

        # Input
        index = self.interference_keycode_to_index.get(keycode, -1)

        # First call
        if not self.is_interfering:
            self.is_interfering = True

            # Form choices
            self.interference_location_choices.clear()
            for entity_id in self.sim_root.children.keys():
                self.interference_location_choices.append(entity_id)

            self.draw()
            return

        # Select location
        if not self.is_spawning:

            # Back
            if keycode == keyboard.key_to_scan_codes("esc")[0]:
                self.is_interfering = False

            # Location
            if 0 <= index < len(self.interference_location_choices):
                self.is_spawning = True
                self.interference_location = self.sim_root.children[self.interference_location_choices[index]]

            self.draw()
            return

        # Select entity
        # Back
        if keycode == keyboard.key_to_scan_codes("esc")[0]:
            self.is_spawning = False

        # Location
        if 0 <= index < len(self.interference_spawn_options):
            entity_type = self.interference_spawn_options[index]
            entity = activator.create_instance(entity_type, ())
            self.interference_location.add_children(entity)

        self.draw()
        return

    #endregion


if __name__ == "__main__":
    Lab1().main()
