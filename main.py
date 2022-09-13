from flask import Flask
from ask_sdk_core.skill_builder import SkillBuilder
from flask_ask_sdk.skill_adapter import SkillAdapter

from ask_sdk_core.utils import is_request_type, is_intent_name, get_slot_value
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
import string
import MicroConnect

sb = SkillBuilder()


# Register all handlers, interceptors etc.
# For eg : sb.add_request_handler(LaunchRequestHandler())

@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "Welcome to MicroStrategy dashboards"
    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Alexa demo", speech_text)).set_should_end_session(
        False)
    return handler_input.response_builder.response


@sb.request_handler(
    can_handle_func=lambda handler_input:
    is_intent_name("AMAZON.CancelIntent")(handler_input) or
    is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "Goodbye!"

    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Alexa demo", speech_text))
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("GetValuefromMicroStrategy"))
def getvalue_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    metric = get_slot_value(handler_input=handler_input, slot_name="Metric")
    # por_ahora(handler_input)
    if metric:
        metric = string.capwords(metric)
        value, valuepm = MicroConnect.getanswer(metric)
        percentagechange = (value / valuepm) - 1

        if percentagechange > 0:
            delta = "increase"
        else:
            delta = "decrease"

        speech_text = "The value for " + str(metric) + " is <say-as interpret-as='cardinal'>" + "{:.0f}".format(
            value) + "</say-as>$ that's a " + "{:.0%}".format(percentagechange) + " " + str(
            delta) + " compared to last month <say-as interpret-as='cardinal'> " + "{:.0f}".format(
            valuepm) + "</say-as>$ "
        written_text = "The value for " + str(metric) + " is " + "{:,.0f}".format(
            value) + "$ that's a " + "{:,.0%}".format(percentagechange) + " " + str(
            delta) + " compared to last month  " + "{:,.0f}".format(valuepm) + "$ "
    else:
        speech_text = "I'm sorry, I din't get the metric. Please try again"
        written_text = speech_text

    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Alexa demo", written_text)).set_should_end_session(
        False)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech_text = "You can ask me for any of your business metrics. For example, try asking me for, What's the profit?"

    handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Alexa demo", speech_text)).set_should_end_session(
        False)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_intent_handler(handler_input):
    # type: (HandlerInput) -> Response
    speech = "Sorry, I'm not sure of what you want. Can you please say it again?"
    handler_input.response_builder.speak(speech).ask(speech).set_should_end_session(
        False)
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    # type: (HandlerInput, Exception) -> Response
    # Log the exception in CloudWatch Logs
    print(exception)
    speech = "Sorry, I didn't get it. Can you please say it again?"
    handler_input.response_builder.speak(speech).ask(speech)
    return handler_input.response_builder.response


app = Flask(__name__)
skill_response = SkillAdapter(
    skill=sb.create(), skill_id="amzn1.ask.skill.08c022b1-2a72-49a9-9255-91a627e2bdef", app=app)  # change it

skill_response.register(app=app, route="/")


@app.route("/")
def invoke_skill():
    return skill_response.dispatch_request()


if __name__ == '__main__':
    app.run()
