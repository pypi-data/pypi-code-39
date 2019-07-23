import PySimpleGUI as sg


def initGUI():

    options_frame = (
        sg.Frame(
            title="Options",
            font=("Arial 16"),
            layout=[
                [
                    sg.Text("Output Directory:", font=("Arial 12"), size=(15, 1)),
                    sg.InputText(font=("Arial 12"), key="Output Directory"),
                    sg.FolderBrowse(font=("Arial 12")),
                ],
                [
                    sg.Text("binning", font=("Arial 12"), size=(15, 1)),
                    sg.InputText("2", font=("Arial 12"), key="binning", size=(6, 1)),
                ],
                [
                    sg.Text("power", font=("Arial 12"), size=(15, 1)),
                    sg.InputText("1024", font=("Arial 12"), key="power", size=(6, 1)),
                ],
                [
                    sg.Text("thumb directory", font=("Arial 12"), size=(15, 1)),
                    sg.InputText(font=("Arial 12"), key="thumb"),
                    sg.FolderBrowse(font=("Arial 12")),
                ],
                [
                    sg.Text("dtotal", font=("Arial 12"), size=(15, 1)),
                    sg.InputText(font=("Arial 12"), key="dtotal", size=(6, 1)),
                ],
                [
                    sg.Text("volt", font=("Arial 12"), size=(15, 1)),
                    sg.InputText("300", font=("Arial 12"), key="volt", size=(6, 1)),
                ],
            ],
        ),
    )

    worker_layout = lambda i: [
        [
            sg.Text(f"Worker {i}", font=("Arial 12")),
            sg.Checkbox(
                "enable",
                enable_events=True,
                default=True,
                font=("Arial 12"),
                key=f"w{i}_enabled",
            ),
            sg.Text("Multiplier", font=("Arial 12")),
            sg.Spin(
                list(range(1, 4)),
                initial_value=1,
                font=("Arial 12"),
                key=f"w{i}_multiplier",
            ),
        ],
        [
            sg.Text("temp", font=("Arial 12"), justification="right", size=(15, 1)),
            sg.InputText(font=("Arial 12"), key=f"tmp{i}"),
            sg.FolderBrowse(font=("Arial 12")),
        ],
        [
            sg.Text(
                "GPU",
                font=("Arial 12"),
                justification="right",
                size=(15, 1),
                tooltip="-1 = no GPU; 0 = best GPU; 1+ = GPU index number",
            ),
            sg.InputText("-1", size=(5, 1), font=("Arial 12"), key=f"w{i}_gpu"),
            sg.Text("", size=(2, 1)),
            sg.Text("threads", font=("Arial 12")),
            sg.InputText("5", size=(5, 1), font=("Arial 12"), key=f"w{i}_threads"),
        ],
    ]

    workers_frame = (
        sg.Frame(
            title="Workers",
            font=("Arial 16"),
            layout=[x for i in range(1, 4) for x in worker_layout(i)],
        ),
    )

    layout = [
        [
            sg.Frame(
                "",
                border_width=0,
                layout=[
                    [
                        sg.Text("Watch Directory:", font=("Arial 16"), size=(18, 1)),
                        sg.InputText(font=("Arial 16"), key="Watch Directory"),
                        sg.FolderBrowse(font=("Arial 12")),
                    ],
                    [
                        sg.Text(
                            "Processed Directory:", font=("Arial 16"), size=(18, 1)
                        ),
                        sg.InputText(font=("Arial 16"), key="Processed Directory"),
                        sg.FolderBrowse(font=("Arial 12")),
                    ],
                ],
            ),
            sg.Frame(
                "",
                border_width=0,
                layout=[
                    [
                        sg.Multiline(
                            size=(None, 5),
                            autoscroll=True,
                            font=("Arial 12"),
                            key="gui_log",
                        )
                    ]
                ],
            ),
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
            sg.Text("Shipper", size=(32, 1), justification="center", font=("Arial 16")),
            *[
                sg.Text(
                    f"Worker {i}",
                    size=(32, 1),
                    justification="center",
                    font=("Arial 16"),
                )
                for i in range(1, 4)
            ],
        ],
        [
            sg.Multiline(autoscroll=True, font=("Arial 12"), key="shipper_log"),
            *[
                sg.Multiline(autoscroll=True, font=("Arial 12"), key=f"w{i}_log")
                for i in range(1, 4)
            ],
        ],
    ]

    window = sg.Window("Framewatcher GUI", layout, resizable=True)
    window.Finalize()
    window.Element("Stop").Update(disabled=True)
    return window
