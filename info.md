[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]](hacs)
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

_Component to integrate with [blueprint][blueprint]._

**This component will set up the following platforms.**

Platform | Description
-- | --
`alarm_control_panel` | Switch and sensor for alarm mode in one, supports Armed, Disarmed, ArmedHome and Triggered.

![example][exampleimg]

{% if not installed %}
## Installation

1. Click install to add the component to Hacs (it will be available in `/config/custom_components/tkvw_egardia`)
2. add the following configuration to `configuration.yaml`

```yaml
tkvw_egardia:
  name: Woonveilig      # A free name of your choosing, a alarm_control_panel entity will be created with entityid alarm_control_panel.<name>
  hostname: !secret tkvw_egardia_hostname # The ip adress of your egardia device
  username: !secret tkvw_egardia_username # The username used to login to the woonveilig webportal
  password: !secret tkvw_egardia_password # The password used to login to the woonveilig webportal
```

{% endif %}


## Configuration is done in the UI

<!---->

***

[blueprint]: https://github.com/custom-components/blueprint
[buymecoffee]: https://www.buymeacoffee.com/ludeeus
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/custom-components/blueprint.svg?style=for-the-badge
[commits]: https://github.com/custom-components/blueprint/commits/master
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/custom-components/blueprint.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Joakim%20Sørensen%20%40ludeeus-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/custom-components/blueprint.svg?style=for-the-badge
[releases]: https://github.com/custom-components/blueprint/releases
