cd ../sam
sam deploy --stack-name sc2-tournaments-notifier --s3-bucket sc2-tournaments-notifier --capabilities CAPABILITY_IAM
cd ../scripts