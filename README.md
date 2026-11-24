# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/whale99999/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/whale99999/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A newspaper front page that sums up the world news of Monday 23 November 2026 in one 1024x1024 image: Nvidia bringing back Jensen Huang as chief executive and the 31% share jump as the lead story, with labelled panels on Ukraine sinking a Russian warship in a Libyan port, the COP31 talks ending with no deal, Iran defying the US blockade of the Strait of Hormuz, the CrowdStrike–Zscaler deal, the factory blaze in Indonesia and new US sanctions on Iran, plus an "also today" strip. Every story on the page names its source. The page is composed by compose.py, which draws every illustration in code with PIL, so the image is fully deterministic; the graded program main.ts validates the finished entry.png against the bounty's size and format gate and copies it to the output directory, byte for byte, so every run writes the same image.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=881py9z1&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
