export default function AboutAIPage() {
  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-3xl mx-auto px-6 py-16">
        <h1 className="text-3xl font-bold text-primary mb-8">
          Comment OdooAI utilise l&apos;intelligence artificielle
        </h1>

        <div className="space-y-8 text-gray-700 text-sm leading-relaxed">
          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-3">
              Ce que vous devez savoir
            </h2>
            <ul className="space-y-3">
              <li className="flex gap-3">
                <span className="text-primary font-bold">1.</span>
                <span><strong>Ce n&apos;est PAS un humain.</strong> Toutes les reponses sont generees par une intelligence artificielle (Claude, par Anthropic).</span>
              </li>
              <li className="flex gap-3">
                <span className="text-primary font-bold">2.</span>
                <span><strong>L&apos;IA peut se tromper.</strong> Verifiez toujours les recommandations avant d&apos;agir dans votre Odoo.</span>
              </li>
              <li className="flex gap-3">
                <span className="text-primary font-bold">3.</span>
                <span><strong>Vos donnees sont protegees.</strong> Les informations sensibles (RH, salaires) sont anonymisees avant traitement.</span>
              </li>
              <li className="flex gap-3">
                <span className="text-primary font-bold">4.</span>
                <span><strong>Pas de conseil legal/fiscal.</strong> OdooAI ne remplace pas un expert-comptable ou un avocat.</span>
              </li>
              <li className="flex gap-3">
                <span className="text-primary font-bold">5.</span>
                <span><strong>Vous restez en controle.</strong> OdooAI ne modifie jamais vos donnees. Lecture seule.</span>
              </li>
            </ul>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-3">
              Comment ca fonctionne
            </h2>
            <p>
              OdooAI a analyse le code source complet d&apos;Odoo — 1 218 modules, 5 514 modeles, 21 013 champs. Cette analyse est stockee dans des Knowledge Graphs (representations structurees des fonctionnalites).
            </p>
            <p className="mt-3">
              Quand vous posez une question, OdooAI :
            </p>
            <ol className="list-decimal ml-6 mt-2 space-y-1">
              <li>Detecte le domaine concerne (vente, stock, comptabilite...)</li>
              <li>Charge le profil d&apos;analyse correspondant</li>
              <li>Si vous etes connecte, interroge votre instance Odoo (lecture seule)</li>
              <li>Genere une reponse personnalisee avec des recommandations</li>
            </ol>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-3">
              Protection de vos donnees
            </h2>
            <p>
              Un Security Guardian protege vos donnees a chaque etape :
            </p>
            <ul className="list-disc ml-6 mt-2 space-y-1">
              <li>Les modeles systeme (droits d&apos;acces, regles) sont bloques — l&apos;IA n&apos;y accede jamais</li>
              <li>Les donnees sensibles (noms, emails, salaires) sont anonymisees avant envoi a l&apos;IA</li>
              <li>Chaque requete est validee contre les injections</li>
              <li>Vos identifiants Odoo ne sont jamais stockes</li>
            </ul>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-3">
              Sous-traitant IA
            </h2>
            <p>
              Les reponses sont generees par <strong>Claude</strong> (Anthropic, San Francisco, USA). Anthropic ne stocke pas les donnees des requetes API et ne les utilise pas pour entrainer ses modeles.
            </p>
          </section>

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-3">
              Conformite
            </h2>
            <p>
              OdooAI est classifie comme un systeme IA a <strong>risque limite</strong> selon l&apos;EU AI Act (Reglement 2024/1689). Nos obligations portent sur la transparence — cette page en fait partie.
            </p>
          </section>

          <section className="border-t border-gray-200 pt-6">
            <p className="text-gray-500 text-xs">
              OdooAI n&apos;est pas affilie a Odoo SA. Pour toute question : contact@odooai.com
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
