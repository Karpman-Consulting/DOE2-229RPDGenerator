from interface.main_app_window import MainApplicationWindow


def main(test_mode=False):
    app = MainApplicationWindow(test_mode)
    app.mainloop()


if __name__ == "__main__":
    # main(test_mode=True)
    main()
