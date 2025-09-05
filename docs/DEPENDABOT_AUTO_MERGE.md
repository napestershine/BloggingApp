# Dependabot Auto-Merge Workflow Documentation

This repository includes an automated workflow for merging Dependabot dependency updates with intelligent conflict resolution.

## 🚀 Features

### Automatic Merging
- **Patch Updates** (e.g., 1.0.0 → 1.0.1): ✅ Auto-merged
- **Minor Updates** (e.g., 1.0.0 → 1.1.0): ✅ Auto-merged
- **Major Updates** (e.g., 1.0.0 → 2.0.0): ⚠️ Manual review required

### Conflict Resolution
- Automatically rebases Dependabot PRs on the main branch
- Resolves conflicts in dependency files (`requirements.txt`, `pubspec.yaml`, `pubspec.lock`)
- Prefers Dependabot's version during conflict resolution

### Safety Checks
- Waits for all CI checks to pass before merging
- Only processes PRs created by `dependabot[bot]`
- Uses squash merge for clean commit history
- Provides clear feedback on merge decisions

## 📋 Supported Package Ecosystems

- **Python**: `pip` packages in `/python/requirements.txt`
- **Flutter/Dart**: `pub` packages in `/app/pubspec.yaml`

## 🔧 Configuration

### Dependabot Configuration
Location: `.github/dependabot.yml`

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/python"
    schedule:
      interval: "daily"
    open-pull-requests-limit: 10
    
  - package-ecosystem: "pub"
    directory: "/app"
    schedule:
      interval: "daily"
    open-pull-requests-limit: 10
```

### Workflow Configuration
Location: `.github/workflows/dependabot-auto-merge.yml`

The workflow triggers on:
- Pull request events (opened, synchronize, reopened)
- Pull request reviews
- Check suite completions
- Status updates

## 🛡️ Security Considerations

### Required Permissions
The workflow requires these permissions:
- `contents: write` - To rebase and merge PRs
- `pull-requests: write` - To comment on and merge PRs
- `checks: read` - To verify CI status

### Update Type Detection
The workflow analyzes PR titles to determine update types:

```bash
# Examples:
"Bump fastapi from 0.115.0 to 0.115.1"  → patch  → ✅ Auto-merge
"Bump fastapi from 0.115.0 to 0.116.0"  → minor  → ✅ Auto-merge
"Bump fastapi from 0.115.0 to 1.0.0"    → major  → ⚠️ Manual review
```

## 🔄 Workflow Process

1. **Trigger**: Dependabot creates/updates a PR
2. **Validation**: Check if actor is `dependabot[bot]`
3. **CI Wait**: Wait for all required checks to complete
4. **Conflict Check**: Determine if PR can be merged cleanly
5. **Rebase**: If conflicts exist, attempt automatic rebase on main
6. **Conflict Resolution**: Automatically resolve dependency file conflicts
7. **Version Analysis**: Determine if update is patch/minor/major
8. **Merge Decision**:
   - Patch/Minor: Auto-merge with squash
   - Major: Add comment requesting manual review

## 📊 Monitoring and Debugging

### Check Workflow Runs
Navigate to `Actions` tab in GitHub to see workflow executions.

### Common Scenarios

#### ✅ Successful Auto-Merge
- PR has passing CI checks
- Update is patch or minor version
- No unresolvable conflicts

#### ⚠️ Manual Review Required
- Major version update detected
- Workflow adds comment explaining why manual review is needed

#### ❌ Auto-Merge Failed
- CI checks failing
- Unresolvable merge conflicts
- Non-dependency file conflicts

## 🛠️ Troubleshooting

### Workflow Not Running
- Ensure PR is created by `dependabot[bot]`
- Check that required permissions are granted
- Verify workflow file syntax is valid

### Merge Conflicts
- The workflow attempts automatic resolution for dependency files
- For other conflicts, manual intervention may be required

### CI Checks Hanging
- Workflow waits up to 30 minutes for checks to complete
- Check individual CI workflow logs for issues

## 🔧 Customization

### Modify Auto-Merge Criteria
Edit the workflow file to change which updates are auto-merged:

```yaml
# Currently: auto-merge patch and minor
if [ "$UPDATE_TYPE" = "major" ]; then
  # Skip auto-merge for major updates
```

### Add Additional Package Ecosystems
Add to `.github/dependabot.yml`:

```yaml
- package-ecosystem: "npm"
  directory: "/frontend"
  schedule:
    interval: "daily"
```

### Adjust Conflict Resolution
Modify the conflict resolution logic in the workflow:

```bash
# For specific file types
if [[ "$file" == "package.json" ]]; then
  git checkout --theirs "$file"
fi
```

## 📈 Benefits

- **Reduced Manual Work**: Automatic merging of safe updates
- **Faster Security Updates**: Quick application of patches
- **Consistent Process**: Standardized handling of dependency updates
- **Clean History**: Squash merging keeps commit history tidy
- **Safety First**: Manual review for potentially breaking changes

## 🎯 Best Practices

1. **Monitor Workflow Runs**: Regular check of automation results
2. **Review Major Updates**: Always manually review major version bumps
3. **Test After Merges**: Ensure automated merges don't break functionality
4. **Keep CI Current**: Maintain comprehensive test coverage
5. **Update Workflow**: Periodically review and improve automation logic