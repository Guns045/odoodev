# Backend Structure Document for odoodev

This document lays out a clear, step-by-step view of the planned backend setup for the `odoodev` project. It uses everyday language so that anyone—technical or not—can understand how we’ll build, host, and maintain our Odoo tutorial platform.

## 1. Backend Architecture

**Overall Design**
- We’ll use **Odoo**’s built-in server framework, which follows a modular, Model-View-Controller (MVC) pattern:
  - **Models** handle data and business logic (written in Python).  
  - **Views** define how data is displayed in the browser or mobile app (XML and JavaScript).  
  - **Controllers** process user actions and coordinate between models and views.
- Custom tutorial modules will plug directly into Odoo’s addons folder, so each lesson or tutorial lives as its own module.

**Scalability & Maintainability**
- **Modules** isolate features: easy to add, remove, or upgrade tutorials without affecting the core.  
- **Docker containers** package the Odoo server and its dependencies, making it simple to scale horizontally by running multiple containers behind a load balancer.  
- **External services** (database, cache) are separated from the application container so each can be scaled independently.

**Performance**
- Use **NGINX** as a reverse proxy in front of Odoo for SSL termination and static file caching.  
- Integrate **Redis** for short-term caching of common queries and session data.

## 2. Database Management

**Database Technology**
- We’ll use **PostgreSQL**, the database engine that Odoo officially supports.

**Data Organization**
- **Relational structure**: Stores users, tutorial modules, content pages, and logs in tables with clear relationships.
- **Transactions & ACID compliance** ensure data integrity when multiple users interact with tutorials or modules at once.

**Data Access & Practices**
- Odoo’s built-in ORM (Object-Relational Mapping) handles queries, so developers work with Python objects instead of raw SQL.
- Regular **backups** scheduled daily, stored in a separate, secure storage bucket.

## 3. Database Schema

Below is a simplified, human-friendly view of our key tables. For those familiar with SQL, we’ve included a PostgreSQL version after.

**Human-Readable Table Overview**
- **Tutorial Module**: ID, Title, Description, Author, Version, Status (draft/published)
- **Tutorial Step**: ID, Module ID (links to Tutorial Module), Step Number, Title, Content (rich text)
- **User**: ID, Name, Email, Password Hash, Role (student/author/admin)
- **User Progress**: ID, User ID, Module ID, Step ID, Completed (yes/no), Timestamp

**PostgreSQL Schema**
```sql
CREATE TABLE tutorial_module (
  id SERIAL PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  author_id INTEGER NOT NULL REFERENCES res_users(id),
  version VARCHAR(20) DEFAULT '1.0',
  status VARCHAR(20) DEFAULT 'draft'
);

CREATE TABLE tutorial_step (
  id SERIAL PRIMARY KEY,
  module_id INTEGER NOT NULL REFERENCES tutorial_module(id),
  step_number INTEGER NOT NULL,
  title VARCHAR(200) NOT NULL,
  content TEXT NOT NULL
);

CREATE TABLE user_progress (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES res_users(id),
  module_id INTEGER NOT NULL REFERENCES tutorial_module(id),
  step_id INTEGER NOT NULL REFERENCES tutorial_step(id),
  completed BOOLEAN DEFAULT FALSE,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

> Note: We leverage Odoo’s core `res_users` table for user information, so we don’t recreate user credentials tables.

## 4. API Design and Endpoints

**Approach**
- We use **Odoo’s JSON-RPC** API for standard operations (creating modules, marking steps complete).  
- In addition, we’ll expose a small set of **RESTful** endpoints for easier integration with third-party tools or mobile apps.

**Key Endpoints**
- **GET /api/tutorials**  
  Returns a list of published modules with metadata (title, description, author).
- **GET /api/tutorials/{module_id}/steps**  
  Returns the ordered steps for a specific module.
- **POST /api/tutorials/{module_id}/progress**  
  Records a user’s completion of a step (requires user token).

> All endpoints use **HTTPS** and require a valid Odoo session token or OAuth2 access token.

## 5. Hosting Solutions

**Cloud Provider**
- **Amazon Web Services (AWS)**: reliable, widely used, scalable.

**Architecture on AWS**
- **Elastic Container Service (ECS)** with Fargate: runs Docker containers without server management.  
- **Amazon RDS** for PostgreSQL: managed database with automated backups and patching.  
- **Amazon S3** for storing backup dumps, static assets (images, supplemental files).

**Why This Setup?**
- **Reliability**: AWS services come with built-in SLAs and multi-AZ deployments.  
- **Scalability**: Fargate and RDS can both scale up or down based on demand.  
- **Cost-Effectiveness**: Pay-as-you-go model keeps upfront costs low.

## 6. Infrastructure Components

- **Load Balancer** (AWS ALB): Distributes traffic across multiple Odoo containers, handles SSL.
- **Caching** (Redis via AWS ElastiCache): Speeds up repeated queries and session lookups.  
- **Content Delivery Network (CDN)** (AWS CloudFront): Serves static assets—images, CSS, JS—quickly around the globe.  
- **Container Registry** (AWS ECR): Stores Docker images for Odoo and related services.

These pieces talk to each other like this:
1. User → CloudFront → ALB → Odoo Container  
2. Odoo Container ↔ RDS (PostgreSQL)  
3. Odoo Container ↔ ElastiCache (Redis)  
4. Docker images → ECR → ECS (Fargate)

## 7. Security Measures

- **Authentication**: OAuth2 for third-party apps, Odoo’s session tokens for web access.  
- **Authorization**: Role-based access controls inside Odoo (student, author, admin).  
- **Encryption in Transit**: All traffic over HTTPS (TLS 1.2+).  
- **Encryption at Rest**: RDS encrypted storage, S3 bucket encryption for backups.  
- **Network Security**: VPC with private subnets for RDS/Redis, security groups that only allow needed ports.  
- **Regular Patching**: Automated security updates for the OS and Docker base images.

## 8. Monitoring and Maintenance

**Monitoring Tools**
- **Amazon CloudWatch**: Tracks CPU, memory, container health, database performance.  
- **Sentry**: Captures application errors and exceptions in real time.  
- **Prometheus & Grafana** (optional add-on): For detailed, custom metrics and dashboards.

**Maintenance Practices**
- **Backup Strategy**: Daily RDS snapshots + weekly full database dumps to S3.  
- **Disaster Recovery**: Multi-AZ RDS deployment, container blue/green deploys in ECS.  
- **Log Rotation**: Centralized logs in CloudWatch Logs, retained for at least 30 days.  
- **Dependency Updates**: Scheduled quarterly reviews of Odoo versions and Python library updates.

## 9. Conclusion and Overall Backend Summary

In building out the `odoodev` backend, we rely on the proven Odoo framework, PostgreSQL, and AWS managed services. Our modular design supports adding new tutorials quickly, while Docker containers and ECS ensure we can handle increasing traffic. With a focus on security, automated backups, and real-time monitoring, the system stays robust and reliable. This setup aligns with our goal of delivering a smooth, scalable tutorial platform for Odoo developers everywhere.

With this blueprint in hand, the team can move forward confidently—adding modules, writing tutorials, and extending the platform—knowing the backend will support our users today and grow with us tomorrow.