/**
 * Nashville Dog Training - AI Lead Autoresponder
 *
 * This script monitors Gmail for new leads and auto-responds using Claude.
 *
 * SETUP:
 * 1. Go to script.google.com
 * 2. Create new project, paste this code
 * 3. Add your Claude API key to Script Properties:
 *    - File > Project Settings > Script Properties
 *    - Add: CLAUDE_API_KEY = your_key
 * 4. Run setupTrigger() once to enable auto-checking
 */

const CLAUDE_API_KEY = PropertiesService.getScriptProperties().getProperty('CLAUDE_API_KEY');
const LABEL_PROCESSED = 'AutoResponded';
const BUSINESS_NAME = 'Nashville Dog Training';
const BUSINESS_PHONE = '(615) XXX-XXXX'; // UPDATE THIS

/**
 * Main function - checks for new lead emails and responds
 */
function checkAndRespondToLeads() {
  // Search for unread emails from FormSubmit (lead notifications)
  const threads = GmailApp.search('is:unread subject:"New Lead: Nashville Dog Training" -label:' + LABEL_PROCESSED);

  if (threads.length === 0) {
    Logger.log('No new leads found');
    return;
  }

  // Create label if it doesn't exist
  let label = GmailApp.getUserLabelByName(LABEL_PROCESSED);
  if (!label) {
    label = GmailApp.createLabel(LABEL_PROCESSED);
  }

  threads.forEach(thread => {
    const messages = thread.getMessages();
    const latestMessage = messages[messages.length - 1];

    // Extract lead info from email body
    const leadInfo = parseLeadEmail(latestMessage.getPlainBody());

    if (leadInfo && leadInfo.email) {
      // Generate AI response
      const response = generateAIResponse(leadInfo);

      // Send response email
      sendResponse(leadInfo.email, leadInfo.name, response);

      // Mark as processed
      thread.addLabel(label);
      thread.markAsRead();

      Logger.log('Responded to lead: ' + leadInfo.name + ' (' + leadInfo.email + ')');
    }
  });
}

/**
 * Parse lead information from FormSubmit email
 */
function parseLeadEmail(body) {
  const lines = body.split('\n');
  const lead = {};

  lines.forEach(line => {
    const [key, ...valueParts] = line.split(':');
    const value = valueParts.join(':').trim();

    if (key && value) {
      const keyLower = key.toLowerCase().trim();
      if (keyLower.includes('name')) lead.name = value;
      if (keyLower.includes('email')) lead.email = value;
      if (keyLower.includes('phone')) lead.phone = value;
      if (keyLower.includes('dog')) lead.dogName = value;
      if (keyLower.includes('area')) lead.area = value;
      if (keyLower.includes('struggling') || keyLower.includes('challenge')) lead.struggles = value;
    }
  });

  return lead;
}

/**
 * Generate personalized response using Claude
 */
function generateAIResponse(lead) {
  const prompt = `You are the friendly owner of Nashville Dog Training, a professional in-home dog training service.

A potential client just submitted a consultation request. Write a warm, personalized email response.

Lead information:
- Name: ${lead.name || 'there'}
- Dog's name: ${lead.dogName || 'your dog'}
- Area: ${lead.area || 'Nashville area'}
- What they're struggling with: ${lead.struggles || 'general training'}

Guidelines:
- Be warm and conversational, not salesy
- Acknowledge their specific struggles empathetically
- Briefly mention you can help with their exact issue
- Offer to schedule a free phone consultation
- Keep it under 150 words
- Sign off as "Nashville Dog Training Team"
- Include phone number: ${BUSINESS_PHONE}

Do NOT include a subject line - just the email body.`;

  try {
    const response = UrlFetchApp.fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01'
      },
      payload: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 500,
        messages: [{
          role: 'user',
          content: prompt
        }]
      })
    });

    const result = JSON.parse(response.getContentText());
    return result.content[0].text;

  } catch (error) {
    Logger.log('Claude API error: ' + error);
    // Fallback response
    return getFallbackResponse(lead);
  }
}

/**
 * Fallback response if Claude API fails
 */
function getFallbackResponse(lead) {
  const name = lead.name ? lead.name.split(' ')[0] : 'there';
  const dogName = lead.dogName || 'your pup';

  return `Hi ${name},

Thanks so much for reaching out about ${dogName}! I got your message and I'd love to learn more about what's going on.

I have some availability this week for a free phone consultation where we can talk through everything and figure out the best path forward.

Would you have 15 minutes to chat? Just reply with a couple times that work for you, or give me a call at ${BUSINESS_PHONE}.

Looking forward to connecting!

Nashville Dog Training Team`;
}

/**
 * Send the response email
 */
function sendResponse(toEmail, toName, body) {
  const subject = `Re: Your Nashville Dog Training Consultation Request`;

  GmailApp.sendEmail(toEmail, subject, body, {
    name: BUSINESS_NAME,
    replyTo: 'jmterprises@gmail.com'
  });
}

/**
 * Set up automatic trigger - run this once
 */
function setupTrigger() {
  // Remove existing triggers
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => {
    if (trigger.getHandlerFunction() === 'checkAndRespondToLeads') {
      ScriptApp.deleteTrigger(trigger);
    }
  });

  // Create new trigger - check every 5 minutes
  ScriptApp.newTrigger('checkAndRespondToLeads')
    .timeBased()
    .everyMinutes(5)
    .create();

  Logger.log('Trigger set up successfully! Will check for new leads every 5 minutes.');
}

/**
 * Manual test function
 */
function testResponse() {
  const testLead = {
    name: 'Test Person',
    email: 'jmterprises@gmail.com',
    dogName: 'Buddy',
    area: 'Nashville',
    struggles: 'pulling on leash and jumping on guests'
  };

  const response = generateAIResponse(testLead);
  Logger.log('Generated response:\n' + response);
}
