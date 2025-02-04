from interface.main_application import MainApplication


def main(test_mode=False):

    app = MainApplication(test_mode)
    app.mainloop()


if __name__ == "__main__":
    # main(test_mode=True)
    main()
