# This code is part of Qiskit.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""The phase instructions update the modulation phase of pulses played on a channel.
This includes ``SetPhase`` instructions which lock the modulation to a particular phase
at that moment, and ``ShiftPhase`` instructions which increase the existing phase by a
relative amount.
"""
from typing import Optional, Union, Tuple

from qiskit.circuit import ParameterExpression
from qiskit.pulse.channels import PulseChannel, PulseError
from qiskit.pulse.instructions.instruction import Instruction


class ShiftPhase(Instruction):
    r"""The shift phase instruction updates the modulation phase of proceeding pulses played on the
    same :py:class:`~qiskit.pulse.channels.Channel`. It is a relative increase in phase determined
    by the ``phase`` operand.

    In particular, a PulseChannel creates pulses of the form

    .. math::
        Re[\exp(i 2\pi f jdt + \phi) d_j].

    The ``ShiftPhase`` instruction causes :math:`\phi` to be increased by the instruction's
    ``phase`` operand. This will affect all pulses following on the same channel.

    The qubit phase is tracked in software, enabling instantaneous, nearly error-free Z-rotations
    by using a ShiftPhase to update the frame tracking the qubit state.
    """

    def __init__(
        self,
        phase: Union[complex, ParameterExpression],
        channel: PulseChannel,
        name: Optional[str] = None,
    ):
        """Instantiate a shift phase instruction, increasing the output signal phase on ``channel``
        by ``phase`` [radians].

        Args:
            phase: The rotation angle in radians.
            channel: The channel this instruction operates on.
            name: Display name for this instruction.

        Raises:
            PulseError: If channel is not a PulseChannel.
        """
        if not isinstance(channel, PulseChannel):
            raise PulseError(
                "The `channel` argument to `ShiftPhase` must be of type `channels.PulseChannel`."
            )
        super().__init__(operands=(phase, channel), name=name)

    @property
    def phase(self) -> Union[complex, ParameterExpression]:
        """Return the rotation angle enacted by this instruction in radians."""
        return self.operands[0]

    @property
    def channel(self) -> PulseChannel:
        """Return the :py:class:`~qiskit.pulse.channels.Channel` that this instruction is
        scheduled on.
        """
        return self.operands[1]

    @property
    def channels(self) -> Tuple[PulseChannel]:
        """Returns the channels that this schedule uses."""
        return (self.channel,)

    @property
    def duration(self) -> int:
        """Duration of this instruction."""
        return 0

    def is_parameterized(self) -> bool:
        """Return True iff the instruction is parameterized."""
        return isinstance(self.phase, ParameterExpression) or super().is_parameterized()


class SetPhase(Instruction):
    r"""The set phase instruction sets the phase of the proceeding pulses on that channel
    to ``phase`` radians.

    In particular, a PulseChannel creates pulses of the form

    .. math::

        Re[\exp(i 2\pi f jdt + \phi) d_j]

    The ``SetPhase`` instruction sets :math:`\phi` to the instruction's ``phase`` operand.
    """

    def __init__(
        self,
        phase: Union[complex, ParameterExpression],
        channel: PulseChannel,
        name: Optional[str] = None,
    ):
        """Instantiate a set phase instruction, setting the output signal phase on ``channel``
        to ``phase`` [radians].

        Args:
            phase: The rotation angle in radians.
            channel: The channel this instruction operates on.
            name: Display name for this instruction.
        Raises:
            PulseError: If channel is not a PulseChannel.
        """
        if not isinstance(channel, PulseChannel):
            raise PulseError(
                "The `channel` argument to `SetPhase` must be of type `channels.PulseChannel`."
            )
        super().__init__(operands=(phase, channel), name=name)

    @property
    def phase(self) -> Union[complex, ParameterExpression]:
        """Return the rotation angle enacted by this instruction in radians."""
        return self.operands[0]

    @property
    def channel(self) -> PulseChannel:
        """Return the :py:class:`~qiskit.pulse.channels.Channel` that this instruction is
        scheduled on.
        """
        return self.operands[1]

    @property
    def channels(self) -> Tuple[PulseChannel]:
        """Returns the channels that this schedule uses."""
        return (self.channel,)

    @property
    def duration(self) -> int:
        """Duration of this instruction."""
        return 0

    def is_parameterized(self) -> bool:
        """Return True iff the instruction is parameterized."""
        return isinstance(self.phase, ParameterExpression) or super().is_parameterized()
