"""
knowledge_base.py — AWS Cloud Assistant Knowledge Base
10+ documents covering all major AWS service categories.
"""

DOCUMENTS = [
    {
        "id": "doc_001",
        "topic": "AWS Overview and Regions",
        "text": """Amazon Web Services (AWS) is a collection of remote computing services that together make up
a cloud computing platform offered over the internet. AWS provides on-demand cloud computing
platforms and APIs to individuals, companies, and governments on a metered, pay-as-you-go basis.
AWS is located in nine geographical regions around the world. Each region is wholly contained
within a single country and all of its data and services stay within the designated region.
This ensures compliance with data residency requirements. Within each region, AWS maintains
multiple Availability Zones (AZs), which are isolated locations with their own power, cooling,
and networking. This design provides high availability and fault tolerance for applications.
AWS cloud services can be tailored as per business or organizational needs, making it the
leading cloud platform globally used by startups, enterprises, and government agencies."""
    },
    {
        "id": "doc_002",
        "topic": "AWS EC2 - Elastic Compute Cloud",
        "text": """Amazon Elastic Compute Cloud (Amazon EC2) is an Infrastructure as a Service (IaaS) offering.
It is a web service that provides secure and resizable compute capacity in the cloud.
EC2 allows you to launch virtual servers called instances, configure security and networking,
and manage storage.

Key advantages of EC2:
- Elastic web scale computing: Helps to increase or decrease computing capacity immediately
  based on demand, so you pay only for what you use.
- Flexible cloud hosting: Allows selection of memory configuration, CPU, instance storage
  and boot partition size as per requirement.
- Reliable: Offers a highly reliable environment where replacement instances can be rapidly
  and predictably commissioned, providing SLA of 99.99% availability.
- Secure: Works in conjunction with Amazon VPC to provide robust networking features.
- Inexpensive: Provides a very low on-demand pricing model with no upfront fees.

EC2 instance types include general purpose, compute optimized, memory optimized, and
GPU instances to suit different workloads."""
    },
    {
        "id": "doc_003",
        "topic": "AWS Batch, Elastic Beanstalk, and Lambda",
        "text": """AWS offers several additional compute services beyond EC2:

AWS Batch enables developers and scientists to easily run thousands of batch computing jobs
on AWS. It dynamically provisions the optimal quantity and type of compute resources based
on volume and specific resource requirements of the batch jobs submitted.

AWS Elastic Beanstalk is a Platform as a Service (PaaS) offering. It is an easy-to-use service
for deploying and scaling web applications and services. You simply upload your code and
Elastic Beanstalk automatically handles deployment, from capacity provisioning, load balancing,
and auto-scaling to application health monitoring. You retain full control over the AWS resources.

AWS Lambda is a serverless PaaS offering that lets you run code for virtually any type of
application or backend service without provisioning or managing servers. You pay only for the
compute time you consume. Lambda supports multiple programming languages including Python,
Node.js, Java, and Go. It automatically scales from a few requests per day to thousands per
second. Lambda integrates natively with other AWS services."""
    },
    {
        "id": "doc_004",
        "topic": "Amazon S3 - Simple Storage Service",
        "text": """Amazon Simple Storage Service (Amazon S3) is an object storage service with a simple
web service interface to store and retrieve any amount of data from anywhere on the web.

Key features of Amazon S3:
- Simple: Provides a web-based console for easy management.
- Durable: Provides durable infrastructure to store important data, which is stored
  redundantly across multiple facilities, delivering 99.999999999% (11 nines) durability.
- Scalable: You can store as much data as needed with no upfront capacity commitments.
- Available: Designed for 99.99% availability over a given year and backed by the S3 SLA.
- Secured: Supports data transfer over SSL (HTTPS) and automatic encryption of data
  once uploaded. Supports fine-grained access control through bucket policies and IAM.
- Low cost: Allows storing large amounts of data at very low cost using tiered pricing.

S3 supports various storage classes including S3 Standard, S3 Intelligent-Tiering,
S3 Standard-IA (Infrequent Access), S3 Glacier for archival, and S3 Glacier Deep Archive
for long-term backup at the lowest cost."""
    },
    {
        "id": "doc_005",
        "topic": "Amazon EBS and EFS - Block and File Storage",
        "text": """Amazon Elastic Block Store (Amazon EBS) provides persistent block storage volumes for use
with Amazon EC2 instances. EBS volumes behave like raw, unformatted storage devices,
allowing users to create a file system on top. Each Amazon EBS volume is automatically
replicated within its Availability Zone to protect from component failure.
EBS volumes provide consistent and low-latency performance needed to run workloads.

EBS volume types include:
- General Purpose SSD (gp3, gp2): Balanced price and performance for most workloads.
- Provisioned IOPS SSD (io2, io1): High performance for mission-critical workloads.
- Throughput Optimized HDD (st1): Low cost for frequently accessed, throughput-intensive workloads.
- Cold HDD (sc1): Lowest cost for less frequently accessed workloads.

Amazon Elastic File System (EFS) provides simple, scalable file storage to use with Amazon
EC2 instances. EFS provides a standard file system interface and file system access semantics.
EFS is a fully managed service that grows and shrinks automatically as you add and remove files,
and you pay only for the storage you use."""
    },
    {
        "id": "doc_006",
        "topic": "Amazon Aurora and RDS - Relational Databases",
        "text": """Amazon Aurora is a MySQL-compatible relational database engine (PaaS) that combines the
speed and availability of high-end commercial databases with the simplicity and cost-effectiveness
of open source databases. Aurora is up to 5x faster than standard MySQL databases.

Aurora features:
- High Performance: Delivers up to 5x throughput of standard MySQL on similar hardware.
- High Availability and Durability: Data is replicated across three Availability Zones with
  six copies of your data for 99.99% availability.
- Highly Scalable: Can auto-scale storage from 10GB up to 128TB.
- Highly Secure: Network isolation using Amazon VPC, with encryption at rest and in transit.

Amazon Relational Database Service (RDS) makes it easy to set up, operate, and scale a
relational database in the cloud. It supports multiple database engines including MySQL,
PostgreSQL, Oracle, Microsoft SQL Server, and MariaDB. RDS handles routine database tasks
such as provisioning, patching, backup, recovery, failure detection, and repair."""
    },
    {
        "id": "doc_007",
        "topic": "Amazon DynamoDB - NoSQL Database",
        "text": """Amazon DynamoDB is a fast and flexible NoSQL database service (PaaS) for applications
that need consistent, single-digit millisecond latency at any scale. It is a fully managed
cloud database that supports both document and key-value data models.

DynamoDB key features:
- Consistent Performance: Delivers consistent, single-digit millisecond response times
  at any scale, with SLA of 99.99% availability.
- Flexible: Supports both document and key-value data models, making it suitable for
  mobile, web, gaming, ad tech, IoT, and many other applications.
- Highly Scalable: Automatically scales tables up and down to adjust for capacity and
  maintain performance. Tables can scale to handle more than 10 trillion requests per day.
- Event Driven Programming: DynamoDB Streams captures table activity including all writes,
  enabling event-driven application architectures with AWS Lambda.

DynamoDB is ideal for use cases like user profiles, shopping carts, game leaderboards,
session management, and real-time analytics."""
    },
    {
        "id": "doc_008",
        "topic": "AWS Migration - Amazon Snowball",
        "text": """Amazon Snowball is a large-scale data transport solution that uses secure appliances
to transfer large amounts of data into and out of AWS. Snowball addresses common challenges
with large-scale data transfers including high network costs, long transfer times,
and security concerns. Transferring data with Snowball is simple, fast, secure,
and can be as little as one-fifth the cost of high-speed internet.

Amazon Snowball key features:
- Fast Performance: Snowball uses multiple layers of protection and an industry-standard
  Trusted Platform Module (TPM) to ensure security, and can transfer 80TB of data in
  approximately 5 to 7 days.
- Highly Secured: Uses 256-bit encryption, a tamper-evident enclosure, and a Trusted
  Platform Module (TPM). All data is encrypted before the appliance leaves your premises.
- Cost Effective: Typically reduces the time to migrate data compared to doing so over
  the internet, reducing data transfer costs by eliminating network fees.

AWS also offers Snowball Edge, which adds local computing capabilities, and Snowmobile,
an exabyte-scale data transfer service for extremely large migrations."""
    },
    {
        "id": "doc_009",
        "topic": "AWS Networking - VPC and Direct Connect",
        "text": """AWS Virtual Private Cloud (VPC) lets users provision a logically isolated section of the
AWS cloud where they can launch AWS resources in a virtual network that they define.
Users have complete control over their virtual networking environment, including selection
of IP address range, creation of subnets, and configuration of route tables and network gateways.

VPC features:
- Complete control over your virtual networking environment including IP address ranges,
  subnets, route tables, and network gateways.
- Multiple layers of security including security groups and network access control lists
  to help control access to Amazon EC2 instances in each subnet.
- Can create a hardware Virtual Private Network (VPN) connection between your corporate
  datacenter and VPC, making the cloud an extension of your existing data center.

AWS Direct Connect makes it easier to establish a dedicated network connection from
your premises to AWS. Using Direct Connect, you can establish private connectivity between
AWS and your data center, office, or colocation environment. This can reduce network costs,
increase bandwidth throughput, and provide a more consistent network experience compared
to internet-based connections. Direct Connect supports speeds from 1Gbps to 100Gbps."""
    },
    {
        "id": "doc_010",
        "topic": "AWS Developer Tools - CodeBuild",
        "text": """AWS CodeBuild is a fully managed build service in the cloud. It compiles your source code,
runs unit tests, and produces artifacts that are ready to deploy. With CodeBuild, you don't
need to provision, manage, and scale your own build servers. CodeBuild scales continuously
and processes multiple builds concurrently, so your builds are not left waiting in a queue.

CodeBuild features:
- Fully Managed: No need to set up, patch, update, or manage your own build servers.
- Continuous Scaling: Automatically scales up and down to meet build volume requirements.
- Pay As You Go: Charged only for the build minutes consumed.
- Extensible: Bring your own build tools and programming runtimes using customized
  build environments as Docker images.
- Secure: Build artifacts are encrypted with customer-managed keys.

AWS CodePipeline is a continuous delivery service for fast and reliable application updates.
AWS CodeDeploy automates code deployments to any instance including EC2 and Lambda.
Together, CodeBuild, CodePipeline, and CodeDeploy form a complete CI/CD pipeline."""
    },
    {
        "id": "doc_011",
        "topic": "AWS Management Tools - CloudWatch",
        "text": """AWS CloudWatch is a monitoring and observability service for AWS cloud resources and
applications running on AWS. CloudWatch collects monitoring and operational data in the
form of logs, metrics, and events, providing a unified view of AWS resources,
applications, and services.

CloudWatch key features:
- Collect and Monitor Log Files: Aggregate log data from Amazon EC2 instances, AWS CloudTrail,
  and other sources for analysis and storage.
- Set Alarms: Watch metrics and send notifications or automatically make changes to resources
  when a threshold is breached.
- Automatic Reaction: Automatically react to changes in AWS resources by triggering Lambda
  functions or other automated actions.
- Resource Utilization Visibility: Get information about resource utilization, application
  performance, and operational health for smooth running of applications.
- Dashboards: Create customizable dashboards to visualize metrics and alarms.

CloudWatch can monitor metrics like CPU utilization, network traffic, and disk reads/writes
for EC2 instances. For custom applications, you can publish custom metrics to CloudWatch
and create alarms based on any metric."""
    },
    {
        "id": "doc_012",
        "topic": "AWS Service Categories Overview",
        "text": """AWS offers over 200 cloud services categorized into the following major groups:

1. Compute: EC2, Lambda, Elastic Beanstalk, AWS Batch, ECS, EKS (Kubernetes) — for running
   applications and processing workloads.

2. Storage: S3 (object storage), EBS (block storage), EFS (file storage), Glacier (archival),
   Storage Gateway — for storing data at any scale.

3. Database: Aurora, RDS (relational), DynamoDB (NoSQL), ElastiCache (in-memory),
   Redshift (data warehouse) — managed database solutions.

4. Migration: Snowball, Database Migration Service, Server Migration Service —
   for moving data and workloads to AWS.

5. Networking: VPC, Direct Connect, Route 53 (DNS), CloudFront (CDN), Elastic Load Balancing —
   for network infrastructure and content delivery.

6. Developer Tools: CodeBuild, CodeDeploy, CodePipeline, Cloud9 IDE —
   for CI/CD and software development lifecycle.

7. Management Tools: CloudWatch (monitoring), CloudTrail (auditing), CloudFormation
   (infrastructure as code), Systems Manager — for operations and governance.

8. Security: IAM (Identity and Access Management), KMS (Key Management), Shield (DDoS),
   WAF (Web Application Firewall) — for securing AWS resources."""
    },
]
