# Human-Aware Safety System

**Webcam Person Tracking and Simulated Robot Speed Control with YOLOv8**

A computer vision prototype that detects and tracks people in a webcam stream, estimates proximity from their bounding-box size, and displays a simulated robot operating state. An OpenCV dashboard shows person IDs, status labels, simulated speed, and recent state changes.

## Features

- Person detection using the pretrained YOLOv8 nano model
- Tracking through Ultralytics `model.track(..., persist=True)`
- Color-coded SAFE, WARNING, and DANGER labels
- Aggregate NORMAL, SLOW, or STOP system state
- Simulated speed values of 100, 50, or 0
- Timestamped state-change logging
- Recent-event dashboard panel

## How It Works

For every detected person, the application calculates:

`ratio = person_bounding_box_area / video_frame_area`

The largest risk among visible people determines the displayed system state.

| Bounding-box ratio | Person label | System state | Simulated speed |
|---|---|---|---:|
| Less than 0.04 | SAFE | NORMAL | 100 |
| At least 0.04 and less than 0.08 | WARNING | SLOW | 50 |
| At least 0.08 | DANGER | STOP | 0 |

With no detected people, the state defaults to NORMAL. These values are display values, not measured physical speeds. The code does not send commands to robot hardware.

## Project Files

- `main.py`: camera capture, tracking, state logic, dashboard, and logging
- `yolov8n.pt`: supplied pretrained model weights
- `requirements.txt`: direct dependencies
- `logs/`: runtime event output directory
- `.gitignore`: excludes environments, caches, and generated logs

## Requirements

- Python environment supported by the installed Ultralytics/PyTorch versions
- A webcam available at camera index `0`
- A desktop environment capable of displaying an OpenCV window
- Internet access for initial dependency installation

The dependency list is not a locked reproduction environment. The original archive contained a Windows virtual environment, which has been omitted from this repository. Create a new environment on your own machine.

## Installation

Run the following from the project directory:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

Keep `main.py`, `yolov8n.pt`, and the `logs` directory together, then run:

```bash
python main.py
```

Press **q** in the dashboard window to exit. State changes are appended to `logs/events_log.txt`.

If the webcam does not open, check camera permissions, close other applications using it, or adjust `cv2.VideoCapture(0)` in `main.py` to the appropriate camera index. Run from the project root so relative paths resolve correctly.

## Event Logging

The application logs changes to the aggregate system state. Each line contains the local time, state, current detected track IDs, and simulated speed. It does not log every frame or every change in the visible person IDs.

## Configuration

Edit `main.py` to adjust the camera index, the ratio thresholds `0.04` and `0.08`, or the simulated speed values `100`, `50`, and `0`.

## Limitations

- Bounding-box size is a heuristic for apparent proximity; it does not measure distance in meters.
- Camera angle, focal length, person size, lighting, and occlusion can affect the displayed state.
- Missed detections lead to the default NORMAL state. This prototype is not suitable as the sole control for physical safety.
- The display simulates robot operation; there is no robot controller, calibrated distance estimation, or hardware emergency-stop integration.
- No accuracy, frame-rate, or physical safety validation results are supplied.

## Validation Status

The packaged Python source passed a syntax check. Webcam capture, model inference, and tracking were not exercised during packaging.

## Model Attribution

Person detection uses Ultralytics YOLOv8 and the supplied `yolov8n.pt` weights. The model and dependencies retain their upstream licensing terms. No new license is assigned to the project's source code in this package.
