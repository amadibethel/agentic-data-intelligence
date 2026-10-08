# Heuristic score (not a probability)
Valid email +15; identity supported +20; company supported +25; role supported +25; external source found +10; no contradictions +5. Maximum 100.
VERIFIED requires score >=90 plus identity/company support and no contradiction. PARTIALLY_VERIFIED >=50 absent conflict. Any explicit contradiction is CONFLICT. Otherwise UNVERIFIED. Calibrate against labelled data before production.
