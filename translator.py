# Example using deep_translator (which often wraps the free Google Translate endpoint)
from deep_translator import GoogleTranslator

translated_text = GoogleTranslator(source='auto', target='en').translate(
    'একটি বস্তুর সময়ের সাথে বেগ পরিবর্তনের হার। বস্তুটি যখন যাত্রা শুরু করে তখন এর ত্বরণ ধনাত্মক ছিল কারণ বেগ বৃদ্ধি পেয়ে এরপর সর্বোচ্চ হয়। সর্বোচ্চ বেগ যখন হয় তখন ত্বরণ শূন্য। এরপর আবার বস্তুর মন্দন হতে থাকলে তখন এর ত্বরণ ঋণাত্মক। অর্থাৎ বলা যায়, শুরুতে বস্তুর ত্বরণ ধনাত্মক ছিল।'
)
print(translated_text)