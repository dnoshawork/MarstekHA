# Marstek Venus E 3.0

Intégration Home Assistant pour la batterie Marstek Venus E 3.0.

## Configuration

1. Ajoutez l'intégration via **Paramètres** → **Appareils et services** → **Ajouter une intégration**
2. Recherchez "Marstek Venus E 3.0"
3. Configurez les paramètres :
   - **Adresse IP** : Adresse IP locale de votre batterie
   - **Port** : Port UDP (par défaut : 30000)
   - **Intervalle de mise à jour** : Fréquence de récupération des données (par défaut : 60 secondes)

⚠️ **Attention** : Un intervalle de mise à jour inférieur à 30 secondes peut surcharger la batterie et causer des problèmes de communication.

## Fonctionnalités

- Surveillance en temps réel de l'état de la batterie
- Mécanisme de retry automatique avec backoff exponentiel pour garantir la fiabilité
- Configuration simple via l'interface utilisateur avec validation
- Port et intervalle de mise à jour configurables
- Contrôle du mode de fonctionnement (Auto, AI, Manuel, Passif)
- Support multilingue (EN/FR)

⚠️ **Note** : Le mode Passif ne fonctionne pas comme décrit dans la documentation constructeur. Consultez le README pour plus de détails.

## Capteurs disponibles

- État de charge (%)
- Température de la batterie (°C)
- Tension de la batterie (V)
- Courant de la batterie (A)
- Puissance de la batterie (W)
- Puissance du réseau (W)
- Puissance de charge (W)
- Puissance consommée (W)
- Puissance solaire (W)
- Mode de fonctionnement

Consultez le [README](https://github.com/dnoshawork/MarstekHA) pour plus d'informations.
