# Risks and Ethics: AI Chatbot using Generative AI

| Risk | Mitigation |
|---|---|
| API key leaked to Git | Use `.env`, keep it in `.gitignore`, commit only `.env.example`. |
| Costs grow unexpectedly | Cap `max_tokens`, trim history, set a billing limit. |
| Model gives wrong answers confidently | Add a disclaimer in the UI; use a system prompt that tells it to admit uncertainty. |

## Ethics and responsible-use notes
- Be honest about limitations in the README and report; do not overstate accuracy.
- Use only data you are allowed to use; anonymise any personal information.
- Document who could be harmed by a wrong output and how the design reduces that risk.
