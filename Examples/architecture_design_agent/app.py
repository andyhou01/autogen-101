import os
import sys
import json
import time
from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import threading
import logging
from queue import Queue

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_agents import (
    load_config,
    create_agents,
)
from autogen import GroupChat, GroupChatManager

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global message store
messages_queue = Queue()
all_messages = []
is_conversation_active = False


def message_callback(sender=None, message=None, **kwargs):
    """
    Callback function to capture messages from the agent conversation
    """
    global all_messages
    try:
        logger.info(
            f"Message callback triggered with sender: {sender}, kwargs: {kwargs.keys()}"
        )

        # Get sender name
        if sender and hasattr(sender, "name"):
            sender_name = sender.name
        elif sender:
            sender_name = str(sender)
        else:
            sender_name = "Unknown"

        # Get message content
        if message:
            if isinstance(message, dict):
                content = message.get("content", "")
            else:
                content = str(message)
        else:
            content = "No content"

        logger.info(f"Processing message from {sender_name}: {content[:100]}...")

        # Create message object
        msg = {"sender": sender_name, "content": content}

        # Add message to global store
        messages_queue.put(msg)
        all_messages.append(msg)

        logger.info(
            f"Message collected and stored, current message count: {len(all_messages)}"
        )
    except Exception as e:
        logger.error(f"Error collecting message: {e}", exc_info=True)


def run_conversation(task):
    """Run the agent conversation with the given task"""
    global all_messages, is_conversation_active
    all_messages = []  # Reset messages
    is_conversation_active = True

    # Add initial system message
    all_messages.append({"sender": "System", "content": "Conversation started"})
    logger.info("Added initial system message")

    # Manually add the initial message from the user/client
    user_message = {"sender": "Client", "content": task}
    all_messages.append(user_message)
    logger.info("Added user task message to message store")

    try:
        # Load configuration and create agents
        logger.info("Loading config and creating agents...")
        config = load_config()
        agents = create_agents(config)
        logger.info(f"Created {len(agents)} agents")

        # Custom message monitor to capture conversation
        def monitor_messages(groupchat):
            logger.info("Message monitor initialized")
            last_msg_count = len(groupchat.messages)

            # Check for messages every second
            while is_conversation_active:
                current_count = len(groupchat.messages)
                if current_count > last_msg_count:
                    # New messages have been added
                    new_messages = groupchat.messages[last_msg_count:current_count]
                    logger.info(f"Found {len(new_messages)} new messages in groupchat")

                    for msg in new_messages:
                        try:
                            if (
                                isinstance(msg, dict)
                                and "name" in msg
                                and "content" in msg
                            ):
                                # Format message from groupchat
                                msg_obj = {
                                    "sender": msg["name"],
                                    "content": msg["content"],
                                }
                                all_messages.append(msg_obj)
                                logger.info(f"Added message from {msg['name']}")
                            else:
                                logger.warning(
                                    f"Unexpected message format: {type(msg)}"
                                )
                        except Exception as e:
                            logger.error(
                                f"Error processing message: {e}", exc_info=True
                            )

                    last_msg_count = current_count

                time.sleep(1)

            logger.info("Message monitor stopped")

        # Create group chat with the callback
        logger.info("Creating GroupChat...")
        groupchat = GroupChat(
            agents=agents, messages=[], max_round=15, speaker_selection_method="auto"
        )

        # Set on_new_message callback
        groupchat.on_new_message = message_callback
        logger.info("Message callback registered to GroupChat")

        # Create manager
        manager = GroupChatManager(
            groupchat=groupchat, llm_config={"config_list": config}
        )

        # Start the message monitor in a separate thread
        monitor_thread = threading.Thread(target=monitor_messages, args=(groupchat,))
        monitor_thread.daemon = True
        monitor_thread.start()
        logger.info("Started message monitor thread")

        # Start conversation
        logger.info("Starting architecture design session...")
        agents[0].initiate_chat(manager, message=task)

        # Wait for message monitor to catch up
        time.sleep(2)

        logger.info(f"Conversation completed, collected {len(all_messages)} messages")
        is_conversation_active = False
        return all_messages

    except Exception as e:
        logger.error(f"Error in conversation: {e}", exc_info=True)
        all_messages.append({"sender": "System", "content": f"Error: {str(e)}"})
        is_conversation_active = False
        return all_messages


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start_conversation", methods=["POST"])
def start_conversation():
    try:
        data = request.json
        task = data.get("task", "")

        if not task:
            return jsonify({"error": "Task is required"}), 400

        # Run conversation in a separate thread
        conversation_thread = threading.Thread(target=run_conversation, args=(task,))
        conversation_thread.daemon = True
        conversation_thread.start()

        # Return immediately with initial status
        return jsonify({"status": "started", "message": "Conversation started"})

    except Exception as e:
        logger.error(f"Error starting conversation: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/stream_messages")
def stream_messages():
    """Server-sent events endpoint for streaming messages"""

    def event_stream():
        last_message_count = 0

        while True:
            current_count = len(all_messages)
            # Check if there are new messages
            if current_count > last_message_count:
                # Get only new messages
                new_messages = all_messages[last_message_count:]
                last_message_count = current_count

                logger.info(
                    f"Streaming {len(new_messages)} new messages, total: {current_count}"
                )

                # Send new messages
                data = json.dumps(
                    {"messages": new_messages, "is_active": is_conversation_active}
                )
                yield f"data: {data}\n\n"

            # Check if conversation is finished and all messages sent
            elif (
                not is_conversation_active
                and last_message_count == current_count
                and last_message_count > 0
            ):
                # Send completion notice
                logger.info("Conversation complete, sending completion notice")
                yield f"data: {json.dumps({'complete': True})}\n\n"
                break

            time.sleep(0.5)  # Wait before checking again

    return Response(event_stream(), mimetype="text/event-stream")


@app.route("/get_messages")
def get_messages():
    """Get all messages for initial load or polling"""
    logger.info(f"Responding to /get_messages with {len(all_messages)} messages")
    return jsonify({"messages": all_messages, "is_active": is_conversation_active})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
