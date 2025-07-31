# Deployment Guide for FastAPI with RDS

This guide will help you deploy your FastAPI application to AWS Lambda with RDS database connectivity.

## Prerequisites

1. **AWS CLI configured** with appropriate permissions
2. **Serverless Framework** installed globally: `npm install -g serverless`
3. **RDS PostgreSQL instance** running
4. **VPC and Security Groups** configured for Lambda-RDS communication

## Configuration Steps

### 1. Environment Variables

Create a `.env` file in the root directory with your RDS credentials:

```bash
# PostgreSQL Configuration
POSTGRES_HOST=your-rds-endpoint.region.rds.amazonaws.com
POSTGRES_PORT=5432
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database_name
```

### 2. VPC Configuration

Update the `serverless.yml` file with your VPC details:

```yaml
provider:
  vpc:
    securityGroupIds:
      - sg-xxxxxxxxx  # Your security group ID
    subnetIds:
      - subnet-xxxxxxxxx  # Private subnet IDs (at least 2)
      - subnet-xxxxxxxxx
```

**Important VPC Requirements:**
- Lambda must be in private subnets
- Security group must allow outbound traffic to RDS (port 5432)
- RDS security group must allow inbound traffic from Lambda security group

### 3. RDS Security Group Configuration

Ensure your RDS security group allows inbound connections from your Lambda security group:

```bash
# Add rule to RDS security group
aws ec2 authorize-security-group-ingress \
  --group-id sg-rds-security-group-id \
  --protocol tcp \
  --port 5432 \
  --source-group sg-lambda-security-group-id
```

### 4. Deploy the Application

Run the deployment script:

```bash
./scripts/deploy.sh
```

Or manually deploy:

```bash
# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Deploy
serverless deploy --verbose
```

## Troubleshooting

### Common Issues

1. **Connection Timeout**
   - Check VPC configuration
   - Verify security group rules
   - Ensure Lambda is in private subnets

2. **Permission Denied**
   - Check IAM roles for Lambda
   - Verify RDS security group allows Lambda connections

3. **Environment Variables Not Set**
   - Ensure `.env` file exists and is properly formatted
   - Check that all required variables are set

### Testing the Deployment

After deployment, test your API endpoints:

```bash
# Get the API Gateway URL from the deployment output
curl https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/

# Test database connectivity
curl https://your-api-id.execute-api.us-east-1.amazonaws.com/dev/health
```

## Security Best Practices

1. **Use AWS Secrets Manager** for database credentials instead of environment variables
2. **Enable VPC Flow Logs** to monitor network traffic
3. **Use private subnets** for Lambda functions
4. **Implement proper IAM roles** with least privilege access
5. **Enable CloudTrail** for API Gateway monitoring

## Monitoring

- **CloudWatch Logs**: Monitor Lambda function logs
- **CloudWatch Metrics**: Track function performance
- **RDS Performance Insights**: Monitor database performance
- **VPC Flow Logs**: Monitor network connectivity

## Cost Optimization

1. **Provisioned Concurrency**: For consistent performance
2. **Reserved Concurrency**: To control costs
3. **RDS Reserved Instances**: For predictable database costs
4. **Auto Scaling**: For RDS instance scaling 