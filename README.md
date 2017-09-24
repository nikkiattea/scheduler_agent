SETUP

1. Download scheduler_agent
2. cd scheduler_agent
3. Run setup.sh (curl test content and change permissions on those files)

RUN

1. In terminal 1, start the scheduler with the following command. If no parameters are given, the default will be input.json and output.json. (run "python scheduler.py -h" for usage).
```bash
python scheduler.py -i input.json -o output.json
```
-OR-
```bash
python scheduler.py
```
2. In terminal 2, start the agent with the following command. python agent.py
3. The scheduler and agent should exit cleanly once it has completed the Task Requests from input.json and written the Task Results to output.json.

REQUIREMENTS

1. Please see scheduler_agent.md for requirements.