jobs:
  check-runner-availability:
    runs-on: ubuntu-latest
    outputs:
      runner: ${{ steps.check-runner.outputs.runner }}
    steps:
      - name: Check self-hosted runner availability
        id: check-runner
        run: |
          RUNNER_STATUS=$(curl -s -H "Authorization: token ${{ secrets.GITHUB_TOKEN }}" "https://api.github.com/repos/${{ github.repository }}/actions/runners" | jq '.runners[] | select(.labels[].name == "self-hosted") | .status')
          if [ "$RUNNER_STATUS" == "online" ]; then
            echo "runner=self-hosted" >> $GITHUB_OUTPUT
          else
            echo "runner=ubuntu-latest" >> $GITHUB_OUTPUT
          fi
          
  build:
    needs: check-runner-availability
    runs-on: ${{ needs.check-runner-availability.outputs.runner }}
    steps:
      - name: Run build
        run: echo "Running build on ${{ needs.check-runner-availability.outputs.runner }}"
