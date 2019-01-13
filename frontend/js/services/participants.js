export function getParticipantsWithOffences(participants, dictionaries) {
    let participantsWithOffences = [];

    participants.forEach((participant) => {
        participant.offences.forEach((offenceId) => {
            let offence = dictionaries.offences[offenceId];
            if (offence) {
                participantsWithOffences.push({
                    role: participant.role,
                    offenceName: offence.name,
                });
            }
        });
    });

    return participantsWithOffences;
}
