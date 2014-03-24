


# Here you can specify up to 8 security questions which will be used in the
# process of restoring a password via the recovery function. You could also
# use them to authenticate a person when they are in direct contact with you,
# say, via phone call.
# Once these questions are set and your project is running, you should NOT
# change their meaning (whilst adapting the phrase would cause no problems).
# If you do not have the complete number of 8 questions in use, then you can,
# however, add some more. Do not forget to adapt the setting 'active_questions'.
security_questions = [
    "Most astonishing phenomenon in nature or science, to you?",              #0
    "Place of your youth that you enjoy remembering the most?",               #1
    "Which allegedly serious person in public do you find most ridiculous?",  #2
    "Your favourite peace of human history?",                                 #3
    "The kind of food that was most disgusting to you when you first ate it?",#4
    "[choose something good]",                                                #5
    "[choose something good]",                                                #6
    "[choose something good]"                                                 #7
    ] 

# This option enables you to, for example, use less than 8 security questions.
# Also, if you decide later on that one of the questions was not picked well and
# you want to exclude it, you should exclude it here and LEAVE its entry in the
# 'security_questions'-list above. Otherwise, you would change the indices of the still
# activated questions, and then the database fields will no longer match their 
# descriptions.
active_questions = ()



# The time that needs to pass between sending two tokens (minutes)
password_reset_token_timeout = 10

# The duration for which a token is usable (minutes)
password_reset_token_lifespan = 60