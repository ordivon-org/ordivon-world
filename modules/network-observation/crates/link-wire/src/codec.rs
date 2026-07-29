use crate::WireError;

pub(crate) struct Cursor<'a> {
    bytes: &'a [u8],
    offset: usize,
}

impl<'a> Cursor<'a> {
    pub(crate) const fn new(bytes: &'a [u8]) -> Self {
        Self { bytes, offset: 0 }
    }

    pub(crate) fn read_u8(&mut self) -> Result<u8, WireError> {
        let byte = *self
            .bytes
            .get(self.offset)
            .ok_or(WireError::UnexpectedEof)?;
        self.offset += 1;
        Ok(byte)
    }

    pub(crate) fn read_u16(&mut self) -> Result<u16, WireError> {
        let bytes = self.read_exact(2)?;
        Ok(u16::from_be_bytes([bytes[0], bytes[1]]))
    }

    pub(crate) fn read_u32(&mut self) -> Result<u32, WireError> {
        let bytes = self.read_exact(4)?;
        Ok(u32::from_be_bytes([bytes[0], bytes[1], bytes[2], bytes[3]]))
    }

    pub(crate) fn read_u64(&mut self) -> Result<u64, WireError> {
        let bytes = self.read_exact(8)?;
        Ok(u64::from_be_bytes([
            bytes[0], bytes[1], bytes[2], bytes[3], bytes[4], bytes[5], bytes[6], bytes[7],
        ]))
    }

    pub(crate) fn read_varint(&mut self) -> Result<u64, WireError> {
        let first = self.read_u8()?;
        let length = 1usize << usize::from(first >> 6);
        let mut value = u64::from(first & 0x3f);
        for _ in 1..length {
            value = (value << 8) | u64::from(self.read_u8()?);
        }
        Ok(value)
    }

    pub(crate) fn read_exact(&mut self, length: usize) -> Result<&'a [u8], WireError> {
        let end = self
            .offset
            .checked_add(length)
            .ok_or(WireError::UnexpectedEof)?;
        let bytes = self
            .bytes
            .get(self.offset..end)
            .ok_or(WireError::UnexpectedEof)?;
        self.offset = end;
        Ok(bytes)
    }

    pub(crate) fn read_string(
        &mut self,
        field: &'static str,
        max: usize,
    ) -> Result<String, WireError> {
        let length =
            usize::try_from(self.read_varint()?).map_err(|_| WireError::ValueTooLarge {
                field,
                actual: u64::MAX,
                max: max as u64,
            })?;
        if length > max {
            return Err(WireError::ValueTooLarge {
                field,
                actual: length as u64,
                max: max as u64,
            });
        }
        let bytes = self.read_exact(length)?;
        String::from_utf8(bytes.to_vec()).map_err(|_| WireError::InvalidUtf8)
    }

    pub(crate) fn remaining(&self) -> &'a [u8] {
        &self.bytes[self.offset..]
    }

    pub(crate) fn finish(self) -> Result<(), WireError> {
        if self.offset == self.bytes.len() {
            Ok(())
        } else {
            Err(WireError::TrailingBytes)
        }
    }
}

pub fn encode_varint(value: u64, output: &mut Vec<u8>) -> Result<(), WireError> {
    match value {
        0..=63 => output.push(value as u8),
        64..=16_383 => {
            let encoded = (value as u16) | 0x4000;
            output.extend_from_slice(&encoded.to_be_bytes());
        }
        16_384..=1_073_741_823 => {
            let encoded = (value as u32) | 0x8000_0000;
            output.extend_from_slice(&encoded.to_be_bytes());
        }
        1_073_741_824..=4_611_686_018_427_387_903 => {
            let encoded = value | 0xc000_0000_0000_0000;
            output.extend_from_slice(&encoded.to_be_bytes());
        }
        _ => {
            return Err(WireError::ValueTooLarge {
                field: "varint",
                actual: value,
                max: 4_611_686_018_427_387_903,
            });
        }
    }
    Ok(())
}

pub fn decode_varint(bytes: &[u8]) -> Result<(u64, usize), WireError> {
    let mut cursor = Cursor::new(bytes);
    let value = cursor.read_varint()?;
    Ok((value, bytes.len() - cursor.remaining().len()))
}

pub(crate) fn write_string(
    output: &mut Vec<u8>,
    field: &'static str,
    value: &str,
    max: usize,
) -> Result<(), WireError> {
    if value.len() > max {
        return Err(WireError::ValueTooLarge {
            field,
            actual: value.len() as u64,
            max: max as u64,
        });
    }
    encode_varint(value.len() as u64, output)?;
    output.extend_from_slice(value.as_bytes());
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn varint_round_trips_boundaries() {
        let values = [
            0,
            63,
            64,
            16_383,
            16_384,
            1_073_741_823,
            1_073_741_824,
            4_611_686_018_427_387_903,
        ];

        for value in values {
            let mut encoded = Vec::new();
            encode_varint(value, &mut encoded).expect("encode");
            let (decoded, consumed) = decode_varint(&encoded).expect("decode");
            assert_eq!(decoded, value);
            assert_eq!(consumed, encoded.len());
        }
    }

    #[test]
    fn varint_rejects_values_above_quic_limit() {
        let error =
            encode_varint(4_611_686_018_427_387_904, &mut Vec::new()).expect_err("must reject");
        assert!(matches!(
            error,
            WireError::ValueTooLarge {
                field: "varint",
                ..
            }
        ));
    }
}
