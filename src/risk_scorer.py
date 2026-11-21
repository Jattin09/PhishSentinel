
def calculate_risk(features, phishing_probability):
    """Calculate a transparent URL risk score."""

    risk_score = phishing_probability * 0.60
    reasons = []

    if phishing_probability >= 70:
        reasons.append("High machine-learning phishing probability")

    if features["has_ip_address"]:
        risk_score += 10
        reasons.append("IP address used instead of a domain")

    keyword_count = features["suspicious_keyword_count"]

    if keyword_count > 0:
        risk_score += min(keyword_count * 5, 15)
        reasons.append("Suspicious keywords found in URL")

    if features["subdomain_count"] >= 2:
        risk_score += 5
        reasons.append("Multiple subdomains detected")

    if features["special_character_count"] >= 3:
        risk_score += 5
        reasons.append("Unusual number of special characters")

    if not features["uses_https"]:
        risk_score += 5
        reasons.append("URL does not use HTTPS")

    risk_score = min(round(risk_score), 100)

    if risk_score >= 70:
        risk_level = "High"
    elif risk_score >= 40:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    if not reasons:
        reasons.append("No additional heuristic indicators detected")

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reasons": reasons
    }
