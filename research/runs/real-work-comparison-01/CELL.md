# Serial receiver capture

`cell.py` prepares and records one read-only calibration cell around the frozen release and source-only bridge. It never invokes a provider. The caller operates serially and retains each exact tool result before another invocation. Submission markers are written **before** the caller invokes the tool and mean `may_have_been_sent`; they do not prove provider receipt. Existing marked/incomplete cells are inspected, never automatically resubmitted.

Create a new output directory, specifying the manifest SHA from `release-validation.json`, case, arm and a distinct caller cell identity. `init` retains exact frozen request bytes. `submit` refuses a prior marker and returns the API argument object after recording its hash. After the caller makes exactly that tool invocation, `record --result FILE` retains the complete serialized tool result, a caller interval observation and the derived bridge transition. A valid retrieval creates the next request from the original frozen input plus the cell's complete visible assistant/retrieval transcript. Other cell histories, methodology requests and scoring keys are not carried forward.

Unknown, truncated, malformed or unrecognized results end the cell as incomplete. They are preserved rather than repaired or retried. A valid final answer closes it. Local recovery may reprocess an already retained identical result; this performs no inference and is not a repeated submission. Changed results or request bytes are refused. Caller intervals include caller/tool overhead and are not model compute time. Provider-reported usage and actual model metadata remain in the original result, including missing values.

This is a local serial recorder, not a durable dispatch engine or general at-most-once guarantee. It provides no authentication, cross-process fencing, crash-atomic record set, fsync/power-loss guarantee or remote idempotency contract. Partial files and lost caller acknowledgements require inspection. Copying a cell directory does not authorize another invocation. A caller with unrestricted host access is outside the retrieval boundary.

Run the bridge and recorder tests without inference:

```sh
python3 -m unittest discover -s research/runs/real-work-comparison-01 -p 'test_*.py' -v
```

The fixtures explicitly label their provider payloads as test doubles. Passing them establishes capture/protocol behavior, not actual receiver completion or model performance. No new model runner or scheduler is installed.

Research Delta: this support unit was authored from PR #109 head `d5017db8fe8014d64bf739e4b3d38aeb322c39da` while its second hosted check remained pending. Seven recorder tests and ten bridge tests passed locally; [validation](cell-validation.json) binds the source and commands. No real receiver/scorer was invoked. It is a prerequisite capture tool for the selected case-01/A cell, not evidence that the cell completed. Hosted validation and integration of the dependency remain separate.
