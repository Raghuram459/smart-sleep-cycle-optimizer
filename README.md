# Smart Sleep Cycle Optimizer

A command-line Python tool that helps you plan your sleep around **90-minute sleep cycles**, log your nights, and see how your sleep affects your mood.

## Features

- **Sleep now:** shows the best wake-up times if you go to bed right now
- **Plan bedtime:** enter a target wake-up time and get the best times to fall asleep
- **Age-aware recommendations:** sleep durations adjust for different age groups
- **Weather tip:** fetches the current temperature (via wttr.in) and gives a sleep comfort tip
- **Sleep logging:** saves sleep time, wake time, duration and morning mood to a CSV file
- **Pattern analysis:** average sleep, average mood, personalised habit advice, and a sleep vs mood graph

## How it works

A full sleep cycle lasts about 90 minutes, and waking at the end of a cycle is generally easier than waking in the middle of one. The tool assumes about 15 minutes to fall asleep, then counts back or forward in whole cycles (for example, 7.5 hours is 5 cycles).

## Tech stack

Python, Pandas, Matplotlib, Requests

## Getting started

### Prerequisites

- Python 3.8 or newer
- Git

### Installation

```bash
git clone https://github.com/Raghuram459/smart-sleep-cycle-optimizer.git
cd smart-sleep-cycle-optimizer
pip install -r requirements.txt
```

### Run

```bash
python smart_sleep_optimizer.py
```

## Usage

You will be asked for your name and age, then shown a menu:

```
1. Sleep now (show wake-up times)
2. Plan bedtime (based on wake-up time)
3. Log a sleep session
4. Analyze my sleep patterns
5. Exit
```

Example (option 1, age 19, at 10:30 PM):

```
Current time: 10:30 PM
If you go to bed now, ideal wake-up times are:

 - 06:15 AM (7.5 hrs sleep)
 - 04:45 AM (6.0 hrs sleep)
 - 03:15 AM (4.5 hrs sleep)
```

Times are entered in `HH:MM AM/PM` format, for example `10:30 PM`.

Logged sessions are saved to `sleep_history.csv` in the project folder, which is created automatically on your first log.

## Roadmap

Planned improvements:

- [ ] Refactor into a modular, installable Python package
- [ ] Unit tests and GitHub Actions CI
- [ ] Input validation and dated records
- [ ] SQLite storage
- [ ] Sleep debt and bedtime consistency score
- [ ] Personalised recommendations using ML
- [ ] Streamlit web dashboard

## Disclaimer

This is a personal wellness project, not a medical tool. Sleep needs vary between people. If you have persistent sleep problems, please talk to a doctor.

## License

Released under the [MIT License](LICENSE).
