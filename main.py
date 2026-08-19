from app.app import TrainingPlannerApp
from app.logging_config import configure_logging


def main():
    configure_logging()
    app = TrainingPlannerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
