# Learning — Mobile Engineer (39) — React Native for Web as Alternative to Separate Mobile App
## Date : 2026-03-22 (Sprint 5, session 4)
## Duree : 3 heures

## Ce que j'ai appris

1. **React Native for Web (RNW) permet de partager 70-85% du code entre mobile et web** : le projet maintenu par Meta transpile les composants React Native en composants DOM web. Pour OdooAI, ca signifie qu'on pourrait avoir une app mobile sans maintenir un codebase separe. Cependant, notre frontend est deja en Next.js 14 avec App Router — migrer vers RNW impliquerait de renoncer aux Server Components et au SSR natif de Next.js.

2. **L'approche "progressive" est plus realiste que la migration totale** : partager les composants de logique metier (hooks, stores, API clients) entre Next.js web et React Native mobile, tout en gardant les couches UI separees. Expo Router (v3+) supporte un file-based routing similaire a Next.js App Router, ce qui reduit la friction de navigation.

3. **Les composants de chat sont les plus portables** : un composant de message, une liste de conversation, un input avec suggestions — ces patterns sont quasi identiques sur web et mobile. Les composants Shadcn/ui (web) et les equivalents React Native Paper ou Tamagui (mobile) partagent la meme API mentale, meme si le code diverge.

4. **Expo avec EAS Build simplifie drastiquement le deployment mobile** : pas besoin de Xcode/Android Studio en local. EAS compile dans le cloud, gere les certificats, et deploie sur les stores. Le cout est de 15$/mois pour un projet (plan Production). Pour un MVP mobile, c'est 10x plus rapide que le setup natif.

5. **La PWA reste l'option la plus pragmatique pour le MVP** : avant de lancer une app native, une PWA bien faite (service worker, manifest, push notifications) couvre 90% des besoins d'un Business Analyst mobile. L'etude Sprint 4 (39-pwa-offline-first) a deja pose les bases. React Native for Web devient pertinent quand on a besoin de features natives (notifications push fiables, acces hors-ligne avance, widgets).

## Comment ca s'applique a OdooAI

1. **Strategie mobile en 3 phases** : Phase 1 (Sprint 8-10) PWA avec le frontend Next.js existant — zero cout additionnel. Phase 2 (Sprint 15+) si les metriques montrent >20% d'usage mobile, lancer un projet Expo/React Native qui reutilise les hooks et l'API client TypeScript. Phase 3 (optionnel) evaluer RNW pour unifier les codebase si la maintenance double devient un probleme.

2. **Partager le layer API client des maintenant** : structurer le code TypeScript frontend pour que les hooks de fetch (`useConversations`, `useOdooConnection`, `useChatMessages`) soient dans un package separe (`@odooai/api-client`), independant de React DOM. Ca prepare la reutilisation mobile sans rien changer au web.

3. **Le chat est le premier candidat mobile** : un Business Analyst en deplacement veut poser une question rapide sur son Odoo. Le chat est le use case mobile #1. Concevoir les composants chat avec une abstraction qui separe la logique (messages, streaming, retry) de la presentation (web vs mobile).

## Ce que je recommande

1. **Sprint 7** : Extraire les hooks API et la logique metier du frontend Next.js dans un package `packages/api-client/`. Aucun import de `react-dom` ou `next/` dans ce package. Cout : 4h, zero impact sur le web existant.

2. **Sprint 10** : Lancer la PWA avec manifest, service worker basique, et icone d'installation. Tester sur 10 utilisateurs beta pour mesurer l'usage mobile reel. Cout : 3h.

3. **Sprint 15 (conditionnel)** : Si >20% d'usage mobile mesure, creer le projet Expo avec Expo Router. Premier ecran : le chat qui reutilise `@odooai/api-client`. Estimation : 2 semaines pour un MVP mobile fonctionnel.

## Sources

1. Expo — "Expo Router v3: Universal File-Based Routing" (2025) : https://docs.expo.dev/router/introduction/
2. Nicolas Gallagher — "React Native for Web" (Meta, 2024) : https://necolas.github.io/react-native-web/
3. Vercel — "Progressive Web Apps with Next.js" (2025) : https://nextjs.org/docs/app/building-your-application/configuring/progressive-web-apps
