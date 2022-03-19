from typing import Optional
import keyboard
import animals_sim
from zeroplayer.entities.entity import RootEntity
from zeroplayer.display_chunk import DisplayChunk


class Lab1:

    #region //// Init, Main

    def __init__(self):
        self.__init_sim()

    def main(self):

        # Hook
        keyboard.on_press_key("f5", lambda _: self.draw(), suppress=True)
        keyboard.on_press_key("o", lambda _: self.sim_open(), suppress=True)
        keyboard.on_press_key("s", lambda _: self.sim_save(), suppress=True)
        keyboard.on_press_key("n", lambda _: self.sim_new(), suppress=True)
        keyboard.on_press_key("i", lambda _: self.sim_interfere(), suppress=True)
        keyboard.on_press_key("space", lambda _: self.sim_step(), suppress=True)

        # Initial drawing
        self.draw()

        # Wait for exit
        keyboard.wait("esc")

        # Cleanup
        keyboard.unhook_all()

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

    #region //// Controls and simulation

    sim_root: Optional[RootEntity]

    display_controls: str = "[O] - Open. [S] - Save. [N] - New.\n[Space] - Step single. [I] - Interfer [ESC] - Exit."

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
