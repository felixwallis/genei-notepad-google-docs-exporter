from urllib import response
from bs4 import BeautifulSoup
import re
import json
import openai


h1_text = []
h2_text = []
h3_text = []


def get_headers():
    with open('genei_notepad.html') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        all_text = soup.find_all(text=True)
        h1_elements = soup.find_all('h1')
        h2_elements = soup.find_all('h2')
        h3_elements = soup.find_all('h3')
        global all_text_string
        all_text_string = ''
        for text in all_text:
            all_text_list = []
            rl = re.split(r'\s', text)
            for word in rl:
                if len(word):
                    all_text_list.append(word)
            text = ' '.join(all_text_list)
            all_text_string += text
        for h1_element in h1_elements:
            h1_text_list = []
            rl = re.split(r'\s', h1_element.get_text())
            for word in rl:
                if len(word):
                    h1_text_list.append(word)
            header = ' '.join(h1_text_list)
            h1_text.append(header)
        for h2_element in h2_elements:
            h2_text_list = []
            rl = re.split(r'\s', h2_element.get_text())
            for word in rl:
                if len(word):
                    h2_text_list.append(word)
            header = ' '.join(h2_text_list)
            h2_text.append(header)
        for h3_element in h3_elements:
            h3_text_list = []
            rl = re.split(r'\s', h3_element.get_text())
            for word in rl:
                if len(word):
                    h3_text_list.append(word)
            header = ' '.join(h3_text_list)
            h3_text.append(header)


def get_header_positions():
    global header_positions
    header_positions = []
    if len(h3_text):
        h3_present = True
    else:
        h3_present = False
    for header in h1_text:
        header_position = all_text_string.index(header)
        header_info = {
            'header': header,
            'header_position': header_position,
            'header_type': 'h1',
            'h3_present': h3_present
        }
        header_positions.append(header_info)
    for header in h2_text:
        header_position = all_text_string.index(header)
        header_info = {
            'header': header,
            'header_position': header_position,
            'header_type': 'h2',
            'h3_present': h3_present
        }
        header_positions.append(header_info)
    for header in h3_text:
        header_position = all_text_string.index(header)
        header_info = {
            'header': header,
            'header_position': header_position,
            'header_type': 'h3'
        }
        header_positions.append(header_info)

    header_positions.sort(
        key=lambda item: item['header_position'])


def retrieve_text_between_markers(marker_1, marker_2, header_length):
    text_snippit = ''
    for index, char in enumerate(all_text_string):
        if marker_2 is not None:
            if index >= (marker_1 + header_length) and index < marker_2:
                text_snippit += char
        else:
            if index >= (marker_1 + header_length):
                text_snippit += char
    return text_snippit


def generate_text_snippits():
    global document_outline
    document_outline = []
    for index, header_position in enumerate(header_positions):
        header = {
            'text': header_position['header'],
            'text_type': header_position['header_type']
        }
        document_outline.append(header)

        marker_1 = header_position['header_position']
        if index < len(header_positions) - 1:
            marker_2 = header_positions[index + 1]['header_position']
        else:
            marker_2 = None
        text_snippt = retrieve_text_between_markers(
            marker_1, marker_2, len(header_position['header']))
        text_after_header = {
            'text': text_snippt,
            'text_type': 'unstyled'
        }
        document_outline.append(text_after_header)


def process_document_with_openai():
    api_key = ''
    with open('OpenAI_API_Key.json', 'r') as fp:
        json_data = json.load(fp)
        api_key = json_data['API_Key']
    openai.api_key = api_key

    global processed_document_outline
    processed_document_outline = [{'text': 'The natural condition and its horrors', 'text_type': 'h1'}, {'text': 'the most famous single phrase in Hobbes\'s entire oeuvre is his observation that life in the state of nature is "solitary, poore, nasty, brutish, and short."Hobbes dissented from Aristotle on the substance of human natureAristotle thought that there was some kind of natural attraction toward the good, and toward life in society.Hobbes thinks that at best there is a common aversion to the summum malum, or death, and that we become "apt" for soci- ety only by being socialized into decent conduct.equally important is Hobbes\'s insistence on the natural equality of man- kind.Thinking of humanity as morally, politically, and intellectually on a level reinforced the view that the state rested on universal consent rather than on a tendency toward a natural hierarchy.Hobbes says the heads of all governments live in a state of nature with respect to one another.The state of nature is simply the condition where we are forced into contact with each other in the absence of a superiorauthority that can lay down and enforce rules to govern our behavior toward each other.the state of nature with which Hobbes is concerned is more nearly the condition of civilized people deprived of stable govern- ment than anything else.', 'text_type': 'unstyled', 'processed_text': '\n\n-Hobbes\'s most famous single phrase is his observation that life in the state of nature is "solitary, poore, nasty, brutish, and short."\n-Hobbes dissented from Aristotle on the substance of human nature.\n-Aristotle thought that there was some kind of natural attraction toward the good, and toward life in society. Hobbes thinks that at best there is a common aversion to the summum malum, or death, and that we become "apt" for soci- ety only by being socialized into decent conduct.\n-Equally important is Hobbes\'s insistence on the natural equality of man- kind. Thinking of humanity as morally, politically, and intellectually on a level reinforced the view that the state rested on universal consent rather than on a tendency toward a natural hierarchy.\n-Hobbes says the heads of all governments live in a state of nature with respect to one another.\n-The state of nature is simply the condition where we are forced into contact with each other in the absence of a superior authority that can lay down and enforce rules to govern our behavior toward each other.\n-The state of nature with which Hobbes is concerned is more nearly the condition of civilized people deprived of stable govern- ment than anything else.'}, {'text': "Hobbes's theory", 'text_type': 'h2'}, {'text': 'may be designed around the prob- lem of sustaining and policing a large, prosperous society, where most people are known well only to a few friends but want to trans- act business and hold intellectual converse with distant strangers.Hobbes\'s theoryWhat is Hobbes\'s theory?We are to consider men in an ungov- erned condition:They are rational (able to calculate conse- quences).they are self-interested (in the sense that they ask what good to themselves will be produced by any given out- come)they are vulnerable to one anotherThey are anxious because they have some grasp of cause and effect (they understand the passage of time, and have a sense of their own mortality).Hobbesian man is heed- ful of the future. This means that no present success in obtaining what he needs for survival can reassure him.This is why Hobbes puts "for a generall inclina- tion of all mankind, a perpetual and restless desire of Power after power, that ceaseth only in Death. "Each appears to the other as a threat, and because each appears as a threat, each is a threat.Each of us is a potential threat to everyone else because each of us faces a world in which other people may cause us harm.The reasons for this are threefold:the state of nature is a state of scarcityHumans are diffident.Humans are prideful.these first two reasons for conflict can be dealt with fairly easily.Competition can be dealt with by the achievement of prosperitySimilarly, once there is a system of police, fear makes for peace rather than conflict.The third cause of conflict is not so easily dealt with.Hobbes insists that a peculiarity of human desire is its indeterminacy.one crude test of the value of our desires is the envy of other men.Hence, our desires are only satiable when we come to the top of the heap, and the criterion of success is universal envy. However,vainglory cannot be slaked by prosperity, and it creates a competition that security cannot defuse.The combined pressure of competition, diffidence, and glory leads to the war of all against all, and to a life that is poor, solitary, nasty, brutish, and short.To escape this condition, men must devise insti- tutions that will enforce rules of conduct that ensure peace.To discover what those rules are is to discover the law of nature.', 'text_type': 'unstyled', 'processed_text': "\n\n- Hobbes's theory is about sustaining and policing a large, prosperous society.\n- Most people in this society are known well only to a few friends, but they want to transact business and hold intellectual conversation with distant strangers.\n- The main problems that Hobbesian man faces are competition, diffidence, and glory.\n- These problems can be dealt with fairly easily by the achievement of prosperity and the enforcement of rules of conduct.\n- The main challenge for Hobbesian man is discovering the law of nature."}, {'text': 'The laws of nature', 'text_type': 'h2'}, {'text': 'Hobbes\'s account of the laws of nature is distinctive."A LAW OF NATURE (lex naturalis) is a Precept, or generall Rule, found out by Reason, by which a man is forbidden to do, that, which is destruc- tive of his life, or taketh away the means of preserving the same; and to omit, that, by which he thinketh it may be best preserved."Hobbes claims that we can see that the rules we out to follows lay down thatwe must preserve our lives, and that we have an absolute right to do whatever conduces to that end.The best way to preserve our lives is through peace.Hobbes argues that the best way for us to achieve peace is for us to renounce all our rights save ony save only the right to defend ouselves in extremis.', 'text_type': 'unstyled', 'processed_text': "\n\n-Hobbes's account of the laws of nature are distinctive in that he believes that we can see that the rules we ought to follow lay down that we must preserve our lives.\n-He also believes that we have an absolute right to do whatever conduces to that end and that the best way to preserve our lives is through peace."}, {'text': 'The contractual escape route', 'text_type': 'h1'}, {'text': 'Hobbes\'s first two laws of nature tell us to seek peace and to be ready to give up as much of our right as others are for the sake of peace.The third law of nature is "that men perform their covenants made."This law is central to the entire edifice.A covenant says now what we shall do in some future timeThe reason for Hobbes\'s concern with covenants is obvious enough.If we are to escape from the state of nature, it can only be by laying aside our "right to all things."we can do that only by covenanting not to do in future what we had a right to do in the past -mainly, by agreeing not to use and act on our private judgment of what conduces to our safety in contradiction of the sovereign\'s public judg- ment, save in dire emergency.Hobbes sees that there are difficulties in the way of contracting out of war and into peaceSince we are obliged not to endanger our lives, we shall not keep covenants that threaten our safety, and a covenant to disarm would do that unless we could rely on everyone else keeping their covenant to disarm too.How can we do this if there is no power to make others keep their covenenats?to establish a power that can make us all keep our covenants, we must covenant to set it up, but that the covenant to do so is impossible to make in the absence of the power it is supposed to establish.Hobbesunderstood the prob- lem he had posed himself.He did not think that all covenants in the state of nature are rendered void by the absence of an enforcing power.The laws of natureoblige us to intend to do what they require; a person who makes a contract is committed to carry- ing out his side of the agreement if the other party does and if it is safe to do so.If upon making a contract he finds that the other party has indeed performed, and that it is safe to perform himself, then he is obliged to carry out the act.The only conclusive evidence of a sincere recognition of the obligationis acting when it is safe.Can this explain the obligation to obey the sovereign and get out of the state of nature?It isabsurd to imagine that we could literally make the sort of covenant that Hobbes describes as a "Covenant of every man with every man, in such manner, as if every man should say to every man..."However, it is far from absurd to imagine that we could indicate to others that we proposed to acceptsuch-and-such a person or body of persons as an authority until it was proved to be more dangerous to do so than to continue in the state of nature.we do it the entire time inside existing political societies.Ultimately, Hobbes was not anxious about such puzzles, and instead chose to pay more attention to the rights of and duties to sovereigns by acquisition.In general, Hobbes aimed to demonstrate the reciprocal relationship between political obedience and a peaceful, stable, enriching social environment.When people mutually covenant each to the others to obey a common authority, they have established what Hobbes calls “sovereignty by institution”.When, threatened by a conqueror, they covenant for protection by promising obedience, they have submit- ted to “sovereignty by acquisition”.What Hobbes imagined was the situation in which we find our- selves after the end of a war or the end of a decisive battle at the absolute mercy of the victor. He is entitled to kill us if he wishes; we are in a state of nature with respect to him; we are, to use Hobbes\'s terminology, an enemy.This does not mean someone ac- tually engaged in fighting him, but someone who is not pledged not to fight him.The victor has the right of nature to do whatever seems good to him to secure himself, and killing us to be on the safe side is no injustice to us.Such a victor may offer us our lvies on the condition that we submit to his authority.Hobbes insists is that if we submit, we are bound. To cite the fact that we submitted out of fear is useless, because we always submit to authority out of fear.The only thing that can void a contract is an event subse- quent to the contract that makes it too dangerous to fulfil itNoth- ing that we could take into account when we made the contract counts against its validity.', 'text_type': 'unstyled', 'processed_text': '\n\n-Hobbes\'s first two laws of nature tell us to seek peace and to be ready to give up as much of our right as others are for the sake of peace. \n-The third law of nature is "that men perform their covenants made."This law is central to the entire edifice. \n-A covenant says now what we shall do in some future time \n-The reason for Hobbes\'s concern with covenants is obvious enough.If we are to escape from the state of nature, it can only be by laying aside our "right to all things."we can do that only by covenanting not to do in future what we had a right to do in the past -mainly, by agreeing not to use and act on our private judgment of what conduces to our safety in contradiction of the sovereign\'s public judg- ment, save in dire emergency. \n-Hobbes sees that there are difficulties in the way of contracting out of war and into peaceSince we are obliged not to endanger our lives, we shall not keep covenants that threaten our safety, and a covenant to disarm would do that unless we could rely on everyone else keeping their covenant to disarm too.How can we do this if there is no power to make others keep their covenenats?to establish a power that can make us all keep our covenants, we must covenant to set it up, but that the covenant to do so is impossible to make in the absence of the power it is supposed to establish. \n-Hobbesunderstood the prob- lem he had posed himself.He did not think that all covenants in the state of nature are rendered void by the absence of an enforcing power. \n-The laws of natureoblige us to intend to do what they require; a person who makes a contract is committed to carrying out his side of the agreement if the other party does and if it is safe to do so.If upon making a contract he finds that the other party has indeed performed, and that it is safe to perform himself, then he is obliged to carry out the act.The only conclusive evidence of a sincere recognition of the obligationis acting when it is safe.Can this explain the obligation to obey the sovereign and get out of the state of nature?It isabsurd to imagine that we could literally make the sort of covenant that Hobbes describes as a "Covenant of every man with every man, in such manner, as if every man should say to every man..."However, it is far from absurd to imagine that we could indicate to others that we proposed to acceptsuch-and-such a person or body of persons as an authority until it was proved to be more dangerous'}, {
        'text': 'Contractualism and obligation', 'text_type': 'h1'}, {'text': "Of all the routes toobligation, contract is at once the most and the least attractive.It is the most attractive because the most conclusive argument for claim- ing that someone has an obligation of some kind is to show them that they imposed it on themselves by some sort of contract-like procedure.It is unat- tractive for the same reason; few of us can recall having promised to obey our rulers for the very good reason that few of us have done so.Hobbes argues thatwhat we pledge is obedience to a person or body of persons, and in doing so we renounce any right to discuss the terms of that obedience thereafter.It is just because we renounce all our rights that Hobbes's theory has the character it does.It seems odd that Hobbes should insist that obedience rests on a covenant, and that he should have argued himself into a corner where he had to give a very counterintuitive account of the way in which coercion does and does not affect the validity of contract.Some aspects of his argument seem easily explicable; they were driven by the political needs of the day.Less explicable is Hobbes's insistence that obligation is self- incurred.This appears to have reflected a deep con- viction that everything in the last resort hinges on the thoughts and actions of individuals.", 'text_type': 'unstyled', 'processed_text': "\n\n-Obligation can come from a contract, which is the most conclusive way to show that someone has an obligation. \n-However, contract is also the least attractive way to become obligated because it's a renunciation of rights. \n-Hobbes argues that what we pledge is obedience to a person or body of persons, and in doing so we renounce any right to discuss the terms of that obedience thereafter. \n-It is just because we renounce all our rights that Hobbes's theory has the character it does. \n-It seems odd that Hobbes should insist that obedience rests on a covenant, and that he should have argued himself into a corner where he had to give a very counterintuitive account of the way in which coercion does and does not affect the validity of contract. \n-Some aspects of his argument seem easily explicable; they were driven by the political needs of the day. \n-Less explicable is Hobbes's insistence that obligation is self-incurred. This appears to have reflected a deep conviction that everything in the last resort hinges on the thoughts and actions of individuals."}, {'text': 'Rights and duties of the soverign', 'text_type': 'h1'}, {'text': 'When the sovereign is instituted, or acquires his power by succession or conquest or some other conventional route, a strikingly lopsided situation arises.We the subjects have nothing but duties toward the sovereign, but he is not in the strict sense under any obligation to us.Hobbes\'s argument for these alarming conclusionshas always struck critics as more bold than convincing.In the case of the sovereign by institution, Hobbes points out that we cove- nant with each other, not with the sovereign.we are contrac- tually obliged to one another to give up our natural rights in the sovereign\'s favor.However, the central issue remains in Hobbes\'s determination to show that the soverign has no obligations to us.In the case of the sovering by acquisition, the contract is made with the sovereign, who does therefore have - momentarily - an obligation to us. However, this obligation can be instantly fulfilled.The sovereign in effect says to us, "If you submit, I will not kill you/\' When he spares us, he has fulfilled his obligation.Our obligation, on the other hand, endures indefinitely.Nonetheless, the sovereign has duties. Indeed, he has obligations to God, although not to any earthly authority.the natural law binds the sovereign, and as long as his or their subjects are more-or- less well behaved, this law binds the sovereign not only in con- science but in action.For all that, Hobbes insists quite energetically both that there is no question of our holding the sovereign to account for anything he might do, and that he should be guided by the moral law.It seems thatHobbes\'s ideal sovereign would be absolute in principle, but indistinguishable from a constitutional sovereign in practice.In other words, we cannot demand a constitutional government as a matter of right. But a ruler, when it is safe to do so, ought to govern in a constitutional fashion.The sovereign\'s duties under the law of nature fall into three roughly distinct categories:First, there are restraints on his actions that stem from the nature of sovereignty, of which the most important are those that forbid the sovereign to divide or limit his sovereign authority.The second class of actions embraces those things that the law of nature forbids or enjoins.The final class of actions refers towhat one might call the standard political tasks that a prudent and effective sovereign will have to perform.Hobbes set out these dutieswith no suggestion that the sovereign\'s political self-control reflects the subject\'s rights.Moreover, Hobbes insists thatwe have no right to have a share in the sovereign authority, and that any system in which we try to set up a collective sovereign embracing many people will almost surely be a disaster.', 'text_type': 'unstyled', 'processed_text': '\n- The sovereign has no obligations to the subjects\n- The sovereign is not bound by the natural law\n- The sovereign has three classes of duties'}, {'text': "Hobbes's definition of liberty", 'text_type': 'h2'}, {'text': 'Hobbes defines liberty in twoways:in the state of nature, "Liberty, is understood, according to the proper significance of the word, the absence of externall impedi- ments."civil liberty, under government, is the absence of law or other sovereign commandment. "The Greatest Liberty of Subjects, dependeth on the Silence of the Law."Both accounts make it entirely possible to act voluntarily but from fear, and neither suggests that freedom has anything to do with the freedom of the will.In this definition, Hobbes wanted to enforce the claim thatfreedom was not a matter of form of government.freedom and government are antithetical, because we give up all our rights when we enter political society, savethe right to defend ourselves against the immediate threat of death and injury.', 'text_type': 'unstyled', 'processed_text': '\n\n- Hobbes defines liberty in two ways: in the state of nature, "Liberty, is understood, according to the proper signification of the word, the absence of externall impedi- ments." \n- Civil liberty, under government, is the absence of law or other sovereign commandment. "The Greatest Liberty of Subjects, dependeth on the Silence of the Law."\n- Both accounts make it entirely possible to act voluntarily but from fear, and neither suggests that freedom has anything to do with the freedom of the will. \n- In this definition, Hobbes wanted to enforce the claim thatfreedom was not a matter of form of government. \n- Freedom and government are antithetical, because we give up all our rights when we enter political society, savethe right to defend ourselves against the immediate threat of death and injury.'}, {'text': 'Resistence', 'text_type': 'h1'}, {'text': "Hobbes was strenuously opposed to many of the things that define liberalism as a political theory.Nonetheless,he held many of the attitudes typical of later defenders of liberal- ism.The sovereign has excellent prudential rea- sons for listening to advisers, allowing much discussion, regulating the affairs of society by general rules rather than particular decreesAllied to the natural law requirement to respect what we might call the subjects moral rights, something close to a liberal regime emerges.However, where Lockeinsists that we enter political society only under the shadow of a natural law whose bonds are drawn tighter by the creation of government, Hobbes relegates that law to the realm of aspiration.If the sovereign breaches it, we are not to resist but to reflect that it is the sovereign whom God will call to account, not ourselves.This is the aspect of Hobbes that many readers find repugnantHobbes takes a view that punishment rests on te soverign's state-of-nature right of self-defence. This has some awkward consequences:we appear to remain in the state of nature vis a vis the sovereign, and that legal relations hold between subject and subject. However, legal relations are not horizontal between the subject and the soverign.Thus, we must abstain from one another's property, but the sovereign is not bound by the same rules.This argument fails todistinguish except in a shadowy fashion between the regular, law-governed treatment of the citizens' property by way of such things as properly legislated taxa- tion, on the one hand, and peremptory expropriation, on the other.The sovereign ought to behave as a constitutional sovereign would be- have, but there is no suggestion that the sovereign must do so for constitutional reasons.Here, Hobbes's system encounters its moment of truth. It is eager to say three things that may not be entirely compatible:First, as long as the sovereign preserves my life and posses- sions, I must assist him to retain his power.Second,I am in the last resort entitled to do whatever seems best to me to save my life.Third,we cannot encourage others to resist the sovereign with us.The conjunction of these last two claims presents problems.The third is inconsistent with theobvious possibility that the best way to secure my- self against the sovereign's ill will is to ally myself with others who can resist him.If we are, for whatever reason, enemies to the sover- eign, we must seek the best way we can find to our own safety.Ultimately, the genius of Hobbes was toproduce a theory that, because it was built on individualist and rationalist foundations, mustleave room not only for individual resistance but also, in extremis, for fully fledged revolution.Levia- thanframed the minds of many gentlemen with a dispositionto ask whether the sovereign had failed to secure our peace and safety or was visibly about to do so.In so doing, it was inadvertently a prop to the revolutionaries of the next fifty years.RephraseSummarise144,914 words left", 'text_type': 'unstyled', 'processed_text': ''}]

    # processed_document_outline = []
    # base_prompt = 'Turn these sentences into bullet points: '
    # for text in document_outline:
    #     if text['text_type'] == 'unstyled':
    #         text_prompt = base_prompt + text['text']
    #         response = openai.Completion.create(
    #             engine="text-davinci-001",
    #             prompt=text_prompt,
    #             temperature=0.7,
    #             max_tokens=1000,
    #             top_p=1,
    #             frequency_penalty=0.5,
    #             presence_penalty=0.2
    #         )
    #         json_object = json.loads(str(response))
    #         text['processed_text'] = json_object['choices'][0]['text']
    #         processed_document_outline.append(text)
    #     else:
    #         processed_document_outline.append(text)


def prep_document_outline_for_google_doc():
    for text_item in processed_document_outline:
        if text_item['text_type'] == 'unstyled':
            text_without_spaced_bullet_points = text_item['processed_text'].replace(
                '\n- ', '\n')
            text_without_all_bullet_points = text_without_spaced_bullet_points.replace(
                '\n-', '\n')
            text_with_cleaned_hyphens = text_without_all_bullet_points.replace(
                '- ', '')
            cleaned_text = re.sub(r'\.(?=\S)([A-Z])', ('. ' + r'\1'),
                                  text_with_cleaned_hyphens)
            text_item['processed_text'] = cleaned_text
    print(processed_document_outline)


get_headers()
get_header_positions()
generate_text_snippits()
process_document_with_openai()
prep_document_outline_for_google_doc()
