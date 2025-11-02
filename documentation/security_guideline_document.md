# Security Guidelines for odoodev

This document outlines essential security principles and best practices for the `odoodev` repository. As this project will host Odoo development tutorials and code samples, it is critical to embed security considerations throughout content creation, module examples, and infrastructure configurations.

## 1. Security by Design

- **Early Integration**: Introduce security topics in every tutorial from the first lesson (e.g., handling user input, access control in Odoo models).  
- **Threat Modeling**: For each module example, identify potential attack vectors (SQL injection, XSS, improper ACLs) and demonstrate how to mitigate them.

## 2. Least Privilege

- **Odoo User Roles**: Showcase how to configure Odoo users and record rules with minimal permissions necessary for a given operation.  
- **Database Accounts**: In tutorials that connect to external databases, advise using database credentials with read/write access only to required schemas or tables.

## 3. Defense in Depth

- **Multiple Layers**: Encourage combining server‐side ACLs, record rules, and UI restrictions to protect data in tutorials.  
- **Validation at Every Layer**: Demonstrate server-side validation in Python model methods and client-side validation in form views.

## 4. Input Validation & Output Encoding

- **Parameterized ORM Queries**: Always use the Odoo ORM (`env['model'].search()`, `create()`, etc.) instead of raw SQL.  
- **Sanitize User Input**: In examples involving HTML fields (`fields.Html`), demonstrate using the built‐in sanitizer or a whitelist approach.  
- **Template Security**: When rendering QWeb templates, avoid injecting unsanitized data. Show how to use `t-esc` for safe escaping.

## 5. Authentication & Access Control

- **Odoo Authentication**: Cover secure password policies (minimum length, complexity) in Odoo’s `res.users` configuration.  
- **Session Security**: Highlight the default session management in Odoo, including session timeout settings in `odoo.conf`.  
- **Multi‐Factor Authentication**: Provide guidance or reference modules that implement TOTP SMS/email MFA for Odoo.

## 6. Data Protection & Privacy

- **Encrypt Data in Transit**: Recommend running Odoo behind an HTTPS reverse proxy (e.g., Nginx, HAProxy with TLS 1.2+).  
- **At‐Rest Encryption**: Suggest using disk‐level encryption for database storage in production tutorials.  
- **PII Handling**: For examples that collect personal data, demonstrate data masking in list views and logs.  
- **Secure Password Storage**: Explain Odoo’s use of `bcrypt` for password hashing and the importance of unique salts.

## 7. API & Service Security

- **Rate Limiting**: Show how to configure reverse proxy rate limiting for JSON‐RPC and XML‐RPC endpoints.  
- **CORS Configuration**: If building custom web controllers, illustrate setting restrictive CORS headers.  
- **API Versioning**: Advise structuring custom controllers under versioned URL prefixes (e.g., `/api/v1/`).

## 8. Web Application Security Hygiene

- **CSRF Protection**: Demonstrate inclusion of CSRF tokens in custom form submissions using Odoo’s `csrf_token` mechanism.  
- **Security Headers**: Provide Nginx configuration snippets that enforce `Strict-Transport-Security`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`.

## 9. Infrastructure & Configuration Management

- **Secure Defaults**: In `odoo.conf`, enable `limit_time_cpu`, `limit_time_real`, and disable developer mode in production.  
- **Service Hardening**: Recommend running Odoo under a dedicated system user with minimal file system permissions.  
- **Disable Demo Data**: Advise disabling loading of demonstration modules in production to avoid sample data leaks.

## 10. Dependency & Module Management

- ** vetted Modules**: Encourage using only community modules with active maintenance and clear security track records.  
- **Lockfiles**: Show how to pin Python dependencies in `requirements.txt` and use `pip-compile` for reproducible builds.  
- **Vulnerability Scanning**: Integrate tools like Bandit or Snyk into CI pipelines to detect insecure patterns in Python and JavaScript code.

## 11. CI/CD & DevOps Security

- **Secrets Management**: Use environment variables or a secrets manager rather than committing credentials in the repository.  
- **Automated Tests**: Include security tests in CI (e.g., form field validation, ACL enforcement).  
- **Artifact Signing**: If distributing Odoo modules, sign release packages and verify checksums.

---

By following these guidelines, `odoodev` tutorials will not only teach Odoo development but also instill best-in-class security practices in every lesson. Ensuring that security is treated as a first-class feature will prepare learners to build robust, production-ready Odoo solutions.