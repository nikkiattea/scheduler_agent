For our distributed scheduler architecture, we have chosen to have an agent
process that runs on each node in our network. It listens for connections on
0.0.0.0:3000 from our scheduler. The scheduler will connect and submit tasks
for execution. The agent responds over the same connection with the result of
the task.

There are two data structures involved in our model. A TaskRequest and a
TaskResult. They are defined as follows:

Task Request

```json
{
  "command": ["cmd", "--flag", "argument1", "argument2"],
  "timeout": 60
}
```

Timeout is in seconds. A timeout of 0 or a missing timeout field means there
is no timeout.

Incoming tasks will be newline delimited.

Task Result

```json
{
  "command": ["cmd", "--flag", "argument1", "argument2"],
  "executed_at": 0,
  "duration_ms": 0.0,
  "exit_code": 0,
  "output": "",
  "error": "",
}
```

The `output` field assumes the output of a task is a string.
The `executed_at` field is the current UNIX time.
The `duration_ms` is the time it took to execute the task in milliseconds.
The `exit_code` field is the exit status of the process.

If the task was successfully executed:
  - Record the time the task was executed and put it in the `executed_at` field.
  - Record the duration of execution and put it in the `duration_ms` field.
  - Record the exit status of the subprocess and put it in the `exit_code` field.
  - Capture everything written to STDOUT and put it in the `output` field.

If there was an error executing the task:
 - put the error that occurred in the `error` field
 - Assign the `exit_code` -1.
 - Leave `executed_at` and `duration_ms` as 0 or missing.
 - Leave output empty or missing.

Requirements:

- Accept incoming tasks on 0.0.0.0:3000 TCP
  - Each TaskRequest will be sent as new-line delimited JSON.
  - Return TaskResult as new-line delimited JSON.
  - The client will close the connection based on its own internal timeout.
- For each incoming task request there should be a task result.
- Do not allow multiple tasks to run concurrently
  - If a request is issued before the previous task finishes, return a response
    with the error: "cannot allow concurrent executions"
- If the execution of the task extends beyond the specified timeout, return a
  response with the error: "timeout exceeded"
  
For testing, we've provided you with the following binaries:

* https://storage.googleapis.com/sensu-interview/scheduler-darwin-amd64 
* https://storage.googleapis.com/sensu-interview/cmd-darwin-amd64

It's best if you use them like this:

```
curl -o scheduler https://storage.googleapis.com/sensu-interview/scheduler-darwin-amd64 
curl -o cmd https://storage.googleapis.com/sensu-interview/cmd-darwin-amd64
```

The inputs we give you for testing will expect the `cmd` binary in the working directory for 
your agent. To run the scheduler and test your solution against the input.json file provided,
we recommend downloading this gist as a zip archive (click the "Download ZIP" button at the
top). You can then run the two curl commands in the directory where you expand the zip, and
everything should be ready to go.

If you have any questions, don't hesitate to reach out via e-mail.