import boto3
import datetime;

def lambda_handler(event, context):
    # ct stores current time
    ct = datetime.datetime.now()
    
    # Get the CloudFront distribution ID for the bucket name
    bucket = event['Records'][0]['s3']['bucket']['name']
    print("The bucket name is: " + bucket)
    
    if bucket == "qa-healthui-reclaimz":
        distribution_id = 'EJEKKSW03X2KF'
    elif bucket == "qa-financeui-reclaimz":
        distribution_id = 'ED4FYJ6JXYG0P'
    else:
        print("Bucket is not configured in the lambda function")
        return {
                'statusCode': 404,
                'body': 'CDN invalidation not triggered!'
               }
 
    # List of objects to invalidate (can be URLs or paths)
    objects_to_invalidate = ['/*']
 
    # Create CloudFront client
    cloudfront = boto3.client('cloudfront')
 
    # Create invalidation request
    invalidation_response = cloudfront.create_invalidation(
        DistributionId=distribution_id,
        InvalidationBatch={
            'Paths': {
                'Quantity': len(objects_to_invalidate),
                'Items': objects_to_invalidate
            },
            'CallerReference': f'lambda-{ct}'
        }
    )
 
    # Print invalidation response
    print("Invalidation Response:", invalidation_response)
 
    return {
        'statusCode': 200,
        'body': 'CDN invalidation triggered successfully!'
    }