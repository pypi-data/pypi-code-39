import traceback

from framewatchergui.gui import initGUI
from framewatchergui.run import start_shipper, start_worker, stop_processes
from framewatchergui.log import LogWindowWriter


def main():
    window = initGUI()
    status = "stopped"

    try:
        while True:
            event, values = window.Read()

            if event == "align":
                window.Element("Align Panel").Update(visible=values["align"])

            elif event == "Start":
                print("Starting framewatcher session")
                window.Element("Start").Update(disabled=True)
                window.Element("Stop").Update(disabled=False)

                watch_dir = values["Watch Directory"]
                final_processed_dir = values["Processed Directory"]

                if values["align"]:
                    worker_processes = []
                    if not any(
                        [
                            values["w1_enabled"],
                            values["w2_enabled"],
                            values["w3_enabled"],
                        ]
                    ):
                        print(
                            "At least one worker must be enabled in order to start aligning"
                        )
                        window.Element("Start").Update(disabled=False)
                        window.Element("Stop").Update(disabled=True)
                        continue

                    tmp_not_specified = False
                    for i in range(1, 4):
                        if values[f"w{i}_enabled"]:
                            if not values[f"tmp{i}"].strip():
                                print(
                                    f"temp directory for worker {i} must be specified"
                                )
                                tmp_not_specified = True
                    if tmp_not_specified:
                        window.Element("Start").Update(disabled=False)
                        window.Element("Stop").Update(disabled=True)
                        continue

                    shipper_pr_dirs = []
                    output_dir = values["Output Directory"]
                    binning = values["binning"]
                    power = values["power"]
                    thumb = values["thumb"]
                    dtotal = values["dtotal"]
                    volt = values["volt"]

                    for i in range(1, 4):
                        if values[f"w{i}_enabled"]:
                            tmp = values[f"tmp{i}"]
                            gpu = values[f"w{i}_gpu"]
                            thr = values[f"w{i}_threads"]
                            worker_log = LogWindowWriter(window, f"w{i}_log")
                            worker = start_worker(
                                worker_log,
                                tmp,
                                binning,
                                power,
                                final_processed_dir,
                                output_dir,
                                thumb,
                                dtotal,
                                gpu,
                                thr,
                                volt,
                            )
                            for _ in range(int(values[f"w{i}_multiplier"])):
                                shipper_pr_dirs.append(tmp)
                            worker_processes.append(worker)
                else:
                    pass
                    shipper_pr_dirs = [final_processed_dir]

                shipper_log = LogWindowWriter(window, "shipper_log")
                shipper = start_shipper(shipper_log, watch_dir, *shipper_pr_dirs)
                status = "started"

            elif event == "Stop":
                print("Stopping session")
                window.Element("Start").Update(disabled=False)
                window.Element("Stop").Update(disabled=True)
                stop_processes([shipper] + worker_processes)
                status = "stopped"

            elif event == "Close" or event is None:
                print("Closing gui")
                if status == "started":
                    stop_processes([shipper] + worker_processes)
                window.Close()
                break

    except KeyboardInterrupt:
        if status == "started":
            stop_processes([shipper] + worker_processes)
        print("Received keyboard interrupt; closing")
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        if status == "started":
            stop_processes([shipper] + worker_processes)


if __name__ == "__main__":
    main()
