#!/bin/bash
# Regenerer les 9 BA Profiles avec Sonnet (au lieu de Haiku)
# Cout estime : ~$2 total
# Prerequis : ANTHROPIC_API_KEY dans .env + KGs dans knowledge_store/

set -e

DOMAINS=(
    sales_crm
    supply_chain
    manufacturing
    accounting
    hr_payroll
    project_services
    helpdesk
    ecommerce
    pos
)

echo "=== Regeneration des 9 BA Profiles avec Sonnet ==="
echo "Cout estime : ~\$2"
echo ""

for domain in "${DOMAINS[@]}"; do
    echo "[$domain] Generating..."
    odooai generate-ba "$domain" --save --model claude-sonnet-4-20250514
    echo "[$domain] Done."
    echo ""
done

echo "=== 9 BA Profiles regeneres ==="
echo "Verifiez dans knowledge_store/17.0/_ba_profiles/"
