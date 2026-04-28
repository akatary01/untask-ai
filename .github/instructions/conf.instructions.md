---
name: Configuration Architect
description: Strict guidelines for /conf directory, YAML structure, and the minimalist load_conf parser.
applyTo: "conf/**/*"
---

# /conf Standards & Protocol

### 1. YAML Logical Separation
Identify the most appropriate existing file. **Do not create a new .yaml file** unless it represents an entirely new infrastructure primitive.
- **`base.yaml`**: Core application settings, global flags, and versioning.
- **`network.yaml`**: API endpoints, ports, and connectivity.
- **`bg_tasks.yaml`**: Celery, Redis, and beat schedules.
- **`email.yaml`**: SMTP and mail server settings.
- **`env.yaml`**: Environment-specific overrides.

### 2. YAML Value Formatting
- **Environment Refs**: Use `env:VAR_NAME`.
- **Dynamic Eval**: Wrap expressions in `${...}` (e.g., `${timedelta(minutes=30)}`).
- **Standard Types**: Use native YAML booleans, integers, and strings.

### 3. Code Generation & Refactoring (`__init__.py`)
The `__init__.py` must remain a "naked" implementation. Every character must be planned.
- **No Unnecessary Refactoring**: Reject vague suggestions to add `try/except`, validation, or type-checking.
- **The Wrapper Rule**: **Do not suggest a wrapper function outside of `load_conf`** instead of modifying the core parser as a workaround.
- **Minimalist Error Handling**: If a specific request to add error handling directly to `load_conf` is approved, it must be implemented in the most concise way possible without adding extra lines.
- **Readability**: Refactoring for readability is allowed only if the final code is not significantly longer than the original.
- **No Documentation Bloat**: No docstrings or inline comments.
- **Function Blueprint**:
  ```python
  def load_conf(settings_dict: dict[str, Any], make_upper: bool = False) -> None:
      for key, value in settings_dict.items():
          updated_value = value
          if isinstance(value, dict):
              updated_value = load_conf(value)
          elif isinstance(value, str):
              if value.startswith('env:'):
                  updated_value = os.environ.get(value[4:])
              elif re.match(r'^\$\{.*\}$', value):
                  updated_value = eval(value[2:-1], context)
          if make_upper:
              key = key.upper()
          globals()[key] = updated_value
