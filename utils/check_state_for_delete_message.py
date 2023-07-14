from aiogram.dispatcher import FSMContext


async def check_state_for_delete_message(state: FSMContext) -> bool:
    state_data = await state.get_data()

    if "message_to_delete" in state_data:
        message_to_delete = state_data["message_to_delete"]
        await message_to_delete.delete()

        return True

    return False
