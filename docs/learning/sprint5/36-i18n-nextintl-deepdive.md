# Learning — i18n Lead (36) — Deep Dive into next-intl Implementation Patterns
## Date : 2026-03-21 (Sprint 5, session 2)
## Duree : 3 heures

## Ce que j'ai appris

1. **next-intl s'integre nativement avec App Router** — Depuis la v3, next-intl utilise le
   middleware Next.js pour la detection de locale et le routing. Le pattern recommended est
   `[locale]/` comme segment dynamique racine, avec un `middleware.ts` qui redirige vers la
   locale par defaut. Ca evite les solutions custom de routing i18n.

2. **Le Server Component i18n est le game-changer** — `useTranslations()` fonctionne dans
   les Server Components via `getTranslations()` async. Les traductions sont resolues cote
   serveur, jamais envoyees au client. Ca reduit le bundle JS de 30-50% par rapport aux
   solutions client-only (react-i18next). Pour OdooAI, chaque Ko de bundle compte pour le
   Time to Interactive du chat.

3. **La structure de fichiers ICU MessageFormat est obligatoire** — next-intl utilise ICU
   pour le pluriel, le genre, et les arguments nommes. Le format
   `{count, plural, one {# item} other {# items}}` est plus robuste que les interpolations
   simples. Structurer les JSON de traduction par namespace (common, chat, settings,
   onboarding) evite les fichiers monolithiques.

4. **Le type-safety avec `createTranslator` elimine les cles orphelines** — En generant les
   types TypeScript a partir des fichiers de traduction source (fr.json), on obtient
   l'autocompletion et les erreurs de compilation pour les cles manquantes. C'est critique
   pour eviter les regressions i18n quand l'equipe frontend grandit.

5. **Le "lazy loading" par route reduit le bundle initial** — Charger uniquement les
   traductions necessaires a la route courante via `getMessages()` dans le layout. Pour
   la page chat, on charge `chat.json` + `common.json`. Pour settings, `settings.json` +
   `common.json`. Ca evite de charger 100% des traductions a chaque page.

## Comment ca s'applique a OdooAI

- **Architecture i18n pour le chat conversationnel** — Le chat est le coeur de l'UI. Les
  messages systeme ("Connexion en cours...", "Analyse du schema..."), les labels de l'input,
  les erreurs, et les tooltips doivent etre traduits. Namespace dedie `chat.json` avec ~50
  cles initiales pour fr et en.

- **Locales prioritaires : fr > en > es** — Le marche initial est francophone (integrateurs
  Odoo France/Belgique/Suisse). L'anglais couvre l'international. L'espagnol est le 3eme
  marche Odoo. Deployer fr + en au launch, es au Sprint 10.

- **Les reponses de l'IA restent dans la langue de l'utilisateur** — La locale detectee par
  next-intl est passee au backend via le header `Accept-Language`. L'agent IA recoit cette
  info et repond dans la langue appropriee. Pas de traduction cote frontend des reponses IA.

## Ce que je recommande

1. **Sprint 6 : setup next-intl avec App Router** — Configurer le middleware, le segment
   `[locale]`, et les fichiers `fr.json` / `en.json` avec les namespaces common et chat.
   Activer le type-safety des la premiere ligne.

2. **Sprint 7 : migrer tous les strings hardcodes** — Passer en revue chaque composant
   React et extraire les strings vers les fichiers de traduction. Objectif : zero string
   hardcode dans le code source.

3. **Sprint 8 : CI check sur la completude des traductions** — Script qui compare les cles
   entre `fr.json` et `en.json`. Toute cle manquante bloque le merge. Integrer dans le
   pipeline GitHub Actions existant.

## Sources

- next-intl Documentation — "App Router Integration" (official, Jan Amann, 2025)
- Vercel Blog — "Internationalization in Next.js 14+" (2024)
- ICU MessageFormat — Unicode CLDR specification (unicode.org)
