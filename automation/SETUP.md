# AI Auto-Responder Setup

This automation monitors jmterprises@gmail.com for new leads and sends personalized AI responses.

## How It Works

1. Someone fills out the form on the website
2. FormSubmit.co sends the lead to jmterprises@gmail.com
3. Google Apps Script checks for new leads every 5 minutes
4. Claude generates a personalized response
5. Response is sent automatically

## Setup (5 minutes)

### 1. Get Claude API Key

1. Go to https://console.anthropic.com/
2. Create account or sign in
3. Go to API Keys > Create Key
4. Copy the key (starts with `sk-ant-`)

### 2. Create Google Apps Script

1. Go to https://script.google.com
2. Click "New Project"
3. Delete the default code
4. Copy/paste everything from `gmail-autoresponder.gs`
5. Click the floppy disk icon to save
6. Name it "Nashville Dog Training Autoresponder"

### 3. Add Your API Key

1. In Apps Script, go to Project Settings (gear icon)
2. Scroll to "Script Properties"
3. Click "Add script property"
4. Name: `CLAUDE_API_KEY`
5. Value: your API key from step 1
6. Click Save

### 4. Enable the Trigger

1. In the code editor, find the function dropdown (says "checkAndRespondToLeads")
2. Change it to `setupTrigger`
3. Click Run (play button)
4. Authorize when prompted (click through security warnings - this is your own script)
5. Done! It will now check every 5 minutes.

### 5. Test It

1. Change function dropdown to `testResponse`
2. Click Run
3. Check the Execution Log (View > Execution Log)
4. You should see a sample AI response

## First Form Submission

The first time someone submits the form, FormSubmit.co will send a confirmation email to jmterprises@gmail.com. Click the link to verify, then future submissions work automatically.

## Costs

- **FormSubmit.co**: Free
- **Google Apps Script**: Free
- **Claude API**: ~$0.003 per response (3 cents per 10 leads)

## Customization

Edit `gmail-autoresponder.gs`:

- `BUSINESS_PHONE`: Update with real phone number
- `everyMinutes(5)`: Change check frequency (in setupTrigger function)
- The AI prompt: Modify the prompt in `generateAIResponse()` to change tone/content

## Troubleshooting

**Emails not being sent?**
- Check Execution Log for errors
- Make sure API key is correct
- Verify Gmail permissions were granted

**Wrong emails being processed?**
- The script looks for subject "New Lead: Nashville Dog Training"
- Adjust the search query in `checkAndRespondToLeads()` if needed
