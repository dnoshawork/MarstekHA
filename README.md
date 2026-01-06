# Marstek Venus E 3.0 - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Intégration Home Assistant pour la batterie Marstek Venus E 3.0.

Cette intégration communique avec la batterie via UDP sur le port 30000 et expose toutes les informations importantes comme des capteurs dans Home Assistant.

## Fonctionnalités

- Communication UDP locale avec la batterie
- Mécanisme de retry automatique avec backoff exponentiel (inspiré du script Jeedom)
- Configuration via l'interface utilisateur
- Support HACS pour installation et mises à jour faciles
- Surveillance de tous les paramètres de la batterie

## Capteurs disponibles

L'intégration expose les capteurs suivants :

| Capteur | Description | Unité |
|---------|-------------|-------|
| State of Charge | Niveau de charge de la batterie | % |
| Battery Temperature | Température de la batterie | °C |
| Battery Voltage | Tension de la batterie | V |
| Battery Current | Courant de la batterie | A |
| Battery Power | Puissance de la batterie | W |
| Grid Power | Puissance du réseau | W |
| Load Power | Puissance consommée | W |
| PV Power | Puissance solaire | W |
| Charge Power | Puissance de charge | W |
| Discharge Power | Puissance de décharge | W |
| ES Mode | Mode de fonctionnement | - |

## Installation

### Via HACS (Recommandé)

1. Assurez-vous que [HACS](https://hacs.xyz/) est installé
2. Dans HACS, cliquez sur "Intégrations"
3. Cliquez sur le menu (trois points en haut à droite) et sélectionnez "Dépôts personnalisés"
4. Ajoutez `https://github.com/dnoshawork/MarstekHA` comme dépôt avec la catégorie "Integration"
5. Recherchez "Marstek Venus E 3.0" dans HACS
6. Cliquez sur "Télécharger"
7. Redémarrez Home Assistant

### Installation manuelle

1. Téléchargez le dossier `custom_components/marstek_venus_e3`
2. Copiez-le dans le dossier `custom_components` de votre installation Home Assistant
3. Redémarrez Home Assistant

## Configuration

### Configuration initiale

1. Dans Home Assistant, allez dans **Paramètres** → **Appareils et services**
2. Cliquez sur **Ajouter une intégration**
3. Recherchez "Marstek Venus E 3.0"
4. Configurez les paramètres suivants :
   - **Adresse IP** : L'adresse IP locale de votre batterie (ex: 192.168.0.182)
   - **Port** : Le port UDP de communication (par défaut : 30000)
   - **Intervalle de mise à jour** : Fréquence de récupération des données en secondes (par défaut : 60 secondes)

### Paramètres de configuration

#### Adresse IP
L'adresse IP locale de votre batterie Marstek Venus E 3.0. Il est recommandé de configurer une adresse IP fixe pour votre batterie (via DHCP statique sur votre routeur ou configuration IP fixe sur la batterie).

#### Port UDP
Le port de communication UDP utilisé par la batterie. La valeur par défaut est **30000**. Ne modifiez ce paramètre que si vous avez configuré un port différent sur votre batterie.

#### Intervalle de mise à jour

L'intervalle de mise à jour détermine la fréquence à laquelle Home Assistant interroge la batterie pour récupérer les données.

- **Valeur par défaut** : 60 secondes (recommandé)
- **Valeur minimale recommandée** : 30 secondes

⚠️ **ATTENTION** : Des valeurs inférieures à 30 secondes peuvent :
- Surcharger la batterie avec trop de requêtes
- Causer des problèmes de communication (timeouts, erreurs)
- Affecter la stabilité de la batterie

Si vous constatez des erreurs de communication fréquentes, augmentez l'intervalle de mise à jour à 90 ou 120 secondes.

### Modification des paramètres

Vous pouvez modifier le port et l'intervalle de mise à jour à tout moment :

1. Allez dans **Paramètres** → **Appareils et services**
2. Cliquez sur **Configurer** sur l'intégration Marstek Venus E 3.0
3. Modifiez les valeurs souhaitées
4. L'intégration se rechargera automatiquement avec les nouveaux paramètres

## Mécanisme de Retry

L'intégration utilise un système de retry robuste :

- **Nombre de tentatives** : 3 par défaut
- **Timeout progressif** : 2s, 3s, 4s pour chaque tentative
- **Backoff exponentiel** : 2s, 4s, 8s entre les tentatives
- **Détection d'erreurs** : Détection automatique des erreurs de parsing et retry

Ce système garantit une communication fiable même en cas de problèmes réseau temporaires.

## Configuration réseau

### Port UDP

La batterie Marstek Venus E 3.0 utilise le port UDP **30000** par défaut pour la communication bidirectionnelle. Ce port est configurable dans l'intégration si votre batterie utilise un port différent.

Assurez-vous que :
- Le port configuré (par défaut 30000) est ouvert sur votre pare-feu
- Home Assistant et la batterie sont sur le même réseau local
- L'adresse IP de la batterie est fixe (configurée en DHCP statique ou IP fixe)
- Aucun autre appareil n'utilise le même port sur votre réseau local

## Exemples d'utilisation

### Carte Lovelace

```yaml
type: entities
title: Batterie Marstek Venus E 3.0
entities:
  - entity: sensor.marstek_venus_e_3_0_state_of_charge
  - entity: sensor.marstek_venus_e_3_0_battery_power
  - entity: sensor.marstek_venus_e_3_0_battery_temperature
  - entity: sensor.marstek_venus_e_3_0_grid_power
  - entity: sensor.marstek_venus_e_3_0_pv_power
  - entity: sensor.marstek_venus_e_3_0_es_mode
```

### Automatisation : Alerte batterie faible

```yaml
automation:
  - alias: "Alerte batterie Marstek faible"
    trigger:
      - platform: numeric_state
        entity_id: sensor.marstek_venus_e_3_0_state_of_charge
        below: 20
    action:
      - service: notify.mobile_app
        data:
          title: "Batterie faible"
          message: "La batterie Marstek est à {{ states('sensor.marstek_venus_e_3_0_state_of_charge') }}%"
```

### Automatisation : Alerte température élevée

```yaml
automation:
  - alias: "Alerte température batterie élevée"
    trigger:
      - platform: numeric_state
        entity_id: sensor.marstek_venus_e_3_0_battery_temperature
        above: 45
    action:
      - service: notify.mobile_app
        data:
          title: "Température batterie élevée"
          message: "La batterie Marstek est à {{ states('sensor.marstek_venus_e_3_0_battery_temperature') }}°C"
```

## Contrôle du mode de fonctionnement

L'intégration permet de contrôler le mode de fonctionnement de la batterie via le service `marstek_venus_e3.set_mode`.

### Modes disponibles

| Mode | Valeur | Description |
|------|--------|-------------|
| **Auto** | 0 | La batterie gère automatiquement la charge et la décharge |
| **AI** | 1 | Mode intelligent avec optimisation |
| **Manuel** | 2 | Contrôle manuel de la charge et décharge avec puissances définies |
| **Passif** | 3 | Mode passif sans gestion active |

### Service : Définir le mode

#### Via l'interface Home Assistant

1. Allez dans **Outils de développement** → **Services**
2. Sélectionnez le service `marstek_venus_e3.set_mode`
3. Choisissez votre appareil
4. Sélectionnez le mode souhaité
5. Pour le mode Manuel : définissez les puissances de charge et décharge
6. Cliquez sur **Appeler le service**

#### Exemples YAML

**Passer en mode Auto :**
```yaml
service: marstek_venus_e3.set_mode
data:
  device_id: <votre_device_id>
  mode: "0"
```

**Passer en mode Manuel avec charge à 1000W :**
```yaml
service: marstek_venus_e3.set_mode
data:
  device_id: <votre_device_id>
  mode: "2"
  charge_power: 1000
  discharge_power: 0
```

**Passer en mode Manuel avec décharge à 500W :**
```yaml
service: marstek_venus_e3.set_mode
data:
  device_id: <votre_device_id>
  mode: "2"
  charge_power: 0
  discharge_power: 500
```

### Automatisation : Passer en mode Manuel pendant les heures pleines

```yaml
automation:
  - alias: "Batterie - Mode Manuel heures pleines"
    trigger:
      - platform: time
        at: "17:00:00"
    action:
      - service: marstek_venus_e3.set_mode
        data:
          device_id: <votre_device_id>
          mode: "2"
          discharge_power: 2000
          charge_power: 0
```

### Automatisation : Revenir en mode Auto pendant les heures creuses

```yaml
automation:
  - alias: "Batterie - Mode Auto heures creuses"
    trigger:
      - platform: time
        at: "22:00:00"
    action:
      - service: marstek_venus_e3.set_mode
        data:
          device_id: <votre_device_id>
          mode: "0"
```

### Automatisation : Charge forcée si SOC < 20%

```yaml
automation:
  - alias: "Batterie - Charge forcée si faible"
    trigger:
      - platform: numeric_state
        entity_id: sensor.marstek_venus_e_3_0_state_of_charge
        below: 20
    action:
      - service: marstek_venus_e3.set_mode
        data:
          device_id: <votre_device_id>
          mode: "2"
          charge_power: 3000
          discharge_power: 0
```

### Trouver le device_id

Pour trouver le `device_id` de votre batterie :

1. Allez dans **Paramètres** → **Appareils et services**
2. Cliquez sur votre appareil Marstek Venus E 3.0
3. Cliquez sur les trois points en haut à droite → **Télécharger les diagnostics**
4. Le `device_id` est visible dans les informations de l'appareil

Ou utilisez ce template dans **Outils de développement** → **Modèle** :
```yaml
{{ device_id('Marstek Venus E 3.0') }}
```

## Dépannage

### La batterie n'est pas détectée

1. Vérifiez que la batterie est allumée et connectée au réseau
2. Vérifiez l'adresse IP de la batterie
3. Vérifiez que le port 30000 est accessible
4. Consultez les logs Home Assistant pour plus de détails

### Les valeurs ne se mettent pas à jour

1. Vérifiez l'intervalle de mise à jour dans les options de l'intégration
2. Consultez les logs pour détecter les erreurs de communication
3. Vérifiez la stabilité de votre réseau local

### Consulter les logs

Les logs de l'intégration sont disponibles dans **Paramètres** → **Système** → **Logs**

Recherchez les entrées contenant `marstek_venus_e3` pour voir les détails de communication.

## Développement

Cette intégration est basée sur le [script Jeedom original](https://github.com/dnoshawork/MarstekVenusE3.0_For_Jeedom/blob/main/marstek_udp_client_all_v3.py).

## Support

Si vous rencontrez des problèmes, veuillez ouvrir une issue sur [GitHub](https://github.com/dnoshawork/MarstekHA/issues).

## Licence

Ce projet est sous licence **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**.

### Résumé de la licence

✅ **Vous pouvez** :
- Utiliser ce projet pour un usage **personnel et non-commercial**
- Modifier et améliorer le code
- Partager et redistribuer le projet

❌ **Vous ne pouvez PAS** :
- Utiliser ce projet à des **fins commerciales** sans autorisation écrite
- Déposer des **brevets** basés sur ce travail (seul l'auteur original peut le faire)

📋 **Obligations** :
- Mentionner l'auteur original : **Damien NOBLET**
- Indiquer les modifications effectuées
- Partager vos modifications sous la **même licence**

💼 **Usage commercial** : Pour toute utilisation commerciale, contactez **Damien NOBLET**

📄 Licence complète : [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Crédits

- Script Jeedom original : [MarstekVenusE3.0_For_Jeedom](https://github.com/dnoshawork/MarstekVenusE3.0_For_Jeedom)
