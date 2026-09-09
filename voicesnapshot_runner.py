from aa_discord_voicesnapshot.gateway import VoiceGatewayClient

if __name__ == "__main__":
    client = VoiceGatewayClient()
    client.start()
    client.join()
