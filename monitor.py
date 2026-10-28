import os
import sys

# Pandas 3.x compatibility shim for evidently
try:
    import pandas.core.dtypes.common as _c
    from pandas.api.types import infer_dtype
    if not hasattr(_c, "infer_dtype_from_object"):
        _c.infer_dtype_from_object = infer_dtype
except Exception:
    pass

import pandas as pd

# Adapt imports to match installed evidently version (0.7.x vs 0.4.x)
try:
    from evidently.report import Report
    from evidently.metric_preset import DataDriftPreset
except (ImportError, ModuleNotFoundError):
    from evidently.legacy.report import Report
    from evidently.legacy.metric_preset import DataDriftPreset

# Create reports directory if not present
os.makedirs("reports", exist_ok=True)

# Sample datasets: reference and current greeting lengths
reference_data = pd.DataFrame({"length": [5, 7, 6, 8]})
current_data   = pd.DataFrame({"length": [6, 7, 9, 10]})

# Build and run data drift report
report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=reference_data, current_data=current_data)

output_path = "reports/evidently_report.html"
report.save_html(output_path)
print(f"Evidently report saved to {output_path}")
