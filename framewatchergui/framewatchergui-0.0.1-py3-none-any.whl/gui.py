import PySimpleGUI as sg


def initGUI():

    options_frame = (
        sg.Frame(
            title="Options",
            font=("Arial 16"),
            layout=[
                [
                    sg.Text("Output Directory:", font=("Arial 12")),
                    sg.InputText(font=("Arial 12"), key="Output Directory"),
                    sg.FolderBrowse(font=("Arial 12")),
                ],
                [
                    sg.Text("binning", font=("Arial 12")),
                    sg.InputText("2", font=("Arial 12"), key="binning"),
                ],
                [
                    sg.Text("power", font=("Arial 12")),
                    sg.InputText("1024", font=("Arial 12"), key="power"),
                ],
                [
                    sg.Text("thumb directory", font=("Arial 12")),
                    sg.InputText(font=("Arial 12"), key="thumb"),
                    sg.FolderBrowse(font=("Arial 12")),
                ],
                [
                    sg.Text("dtotal", font=("Arial 12")),
                    sg.InputText("45", font=("Arial 12"), key="dtotal"),
                ],
                [
                    sg.Text("volt", font=("Arial 12")),
                    sg.InputText("300", font=("Arial 12"), key="volt"),
                ],
            ],
        ),
    )

    workers_frame = (
        sg.Frame(
            title="Workers",
            font=("Arial 16"),
            layout=[
                [
                    sg.Text("Worker 1", font=("Arial 12")),
                    sg.Checkbox(
                        "enable",
                        enable_events=True,
                        default=True,
                        font=("Arial 12"),
                        key="w1_enabled",
                    ),
                    sg.Text("Multiplier", font=("Arial 12")),
                    sg.Spin(
                        list(range(1, 4)),
                        initial_value=1,
                        font=("Arial 12"),
                        key="w1_multiplier",
                    ),
                ],
                [
                    sg.Text(""),
                    sg.Text("temp directory", font=("Arial 12")),
                    sg.InputText(font=("Arial 12"), key="tmp1"),
                    sg.FolderBrowse(font=("Arial 12")),
                ],
                [
                    sg.Text(""),
                    sg.Text("GPU", font=("Arial 12")),
                    sg.InputText("-1", size=(5, 1), font=("Arial 12"), key="w1_gpu"),
                ],
                [
                    sg.Text(""),
                    sg.Text("threads", font=("Arial 12")),
                    sg.InputText("5", size=(5, 1), font=("Arial 12"), key="w1_threads"),
                ],
                [
                    sg.Text("Worker 2", font=("Arial 12")),
                    sg.Checkbox(
                        "enable",
                        enable_events=True,
                        default=True,
                        font=("Arial 12"),
                        key="w2_enabled",
                    ),
                    sg.Text("Multiplier", font=("Arial 12")),
                    sg.Spin(
                        list(range(1, 4)),
                        initial_value=1,
                        font=("Arial 12"),
                        key="w2_multiplier",
                    ),
                ],
                [
                    sg.Text(""),
                    sg.Text("temp directory", font=("Arial 12")),
                    sg.InputText(font=("Arial 12"), key="tmp2"),
                    sg.FolderBrowse(font=("Arial 12")),
                ],
                [
                    sg.Text(""),
                    sg.Text("GPU", font=("Arial 12")),
                    sg.InputText("-1", size=(5, 1), font=("Arial 12"), key="w2_gpu"),
                ],
                [
                    sg.Text(""),
                    sg.Text("threads", font=("Arial 12")),
                    sg.InputText("5", size=(5, 1), font=("Arial 12"), key="w2_threads"),
                ],
                [
                    sg.Text("Worker 3", font=("Arial 12")),
                    sg.Checkbox(
                        "enable",
                        enable_events=True,
                        default=True,
                        font=("Arial 12"),
                        key="w3_enabled",
                    ),
                    sg.Text("Multiplier", font=("Arial 12")),
                    sg.Spin(
                        list(range(1, 4)),
                        initial_value=1,
                        font=("Arial 12"),
                        key="w3_multiplier",
                    ),
                ],
                [
                    sg.Text(""),
                    sg.Text("temp directory", font=("Arial 12")),
                    sg.InputText(font=("Arial 12"), key="tmp3"),
                    sg.FolderBrowse(font=("Arial 12")),
                ],
                [
                    sg.Text(""),
                    sg.Text("GPU", font=("Arial 12")),
                    sg.InputText("-1", size=(5, 1), font=("Arial 12"), key="w3_gpu"),
                ],
                [
                    sg.Text(""),
                    sg.Text("threads", font=("Arial 12")),
                    sg.InputText("5", size=(5, 1), font=("Arial 12"), key="w3_threads"),
                ],
            ],
        ),
    )

    layout = [
        [
            sg.Text("Watch Directory:", font=("Arial 16")),
            sg.InputText(font=("Arial 16"), key="Watch Directory"),
            sg.FolderBrowse(font=("Arial 12")),
        ],
        [
            sg.Text("Processed Directory:", font=("Arial 16")),
            sg.InputText(font=("Arial 16"), key="Processed Directory"),
            sg.FolderBrowse(font=("Arial 12")),
        ],
        [
            sg.Checkbox(
                "Align",
                enable_events=True,
                default=True,
                font=("Arial 16"),
                key="align",
            )
        ],
        [
            sg.Frame(
                key="Align Panel",
                title="",
                border_width=0,
                font=("Arial 16"),
                layout=[options_frame, workers_frame],
            )
        ],
        [
            sg.Button("Start", font=("Arial 16"), key="Start"),
            sg.Button("Stop", font=("Arial 16"), key="Stop"),
            sg.Button("Close", font=("Arial 16"), key="Close"),
        ],
        [
            sg.Text("Shipper", size=(40, 1), justification="center", font=("Arial 16")),
            sg.Text(
                "Worker 1", size=(40, 1), justification="center", font=("Arial 16")
            ),
            sg.Text(
                "Worker 2", size=(40, 1), justification="center", font=("Arial 16")
            ),
            sg.Text(
                "Worker 3", size=(40, 1), justification="center", font=("Arial 16")
            ),
        ],
        [
            sg.Multiline(
                size=(36, 5), autoscroll=True, font=("Arial 16"), key="shipper_log"
            ),
            sg.Multiline(
                size=(36, 5), autoscroll=True, font=("Arial 16"), key="w1_log"
            ),
            sg.Multiline(
                size=(36, 5), autoscroll=True, font=("Arial 16"), key="w2_log"
            ),
            sg.Multiline(
                size=(36, 5), autoscroll=True, font=("Arial 16"), key="w3_log"
            ),
        ],
    ]

    window = sg.Window("Framewatcher GUI", layout, resizable=True)
    window.Finalize()
    window.Element("Stop").Update(disabled=True)
    return window
