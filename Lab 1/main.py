from typing import Optional, Callable
import keyboard
import animals_sim
from zeroplayer.entities.entity import RootEntity
from zeroplayer.display_chunk import DisplayChunk


class Lab1:

    #region //// Init, Main

    def __init__(self):
        self.__init_sim()

    def main(self):

        # Initial drawing
        self.draw()

        # Map input methods
        self.forward_rules_fill()

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

        # Controls
        print(self.display_controls)

    #endregion

    #region //// Controls

    forward_rules: dict[int, Callable[[], None | bool]]
    display_controls: str = "[O] - Open. [S] - Save. [N] - New.\n[Space] - Step single. [I] - Interfer [ESC] - Exit."

    def forward_rules_fill(self) -> None:
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

    def sim_interfere(self):
        raise NotImplementedError

    #endregion


if __name__ == "__main__":
    Lab1().main()
