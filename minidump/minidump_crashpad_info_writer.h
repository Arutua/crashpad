// Copyright 2014 The Crashpad Authors. All rights reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef CRASHPAD_MINIDUMP_MINIDUMP_CRASHPAD_INFO_WRITER_H_
#define CRASHPAD_MINIDUMP_MINIDUMP_CRASHPAD_INFO_WRITER_H_

#include <vector>

#include "base/basictypes.h"
#include "base/memory/scoped_ptr.h"
#include "minidump/minidump_extensions.h"
#include "minidump/minidump_stream_writer.h"

namespace crashpad {

class MinidumpModuleCrashpadInfoListWriter;

//! \brief The writer for a MinidumpCrashpadInfo stream in a minidump file.
class MinidumpCrashpadInfoWriter final : public internal::MinidumpStreamWriter {
 public:
  MinidumpCrashpadInfoWriter();
  ~MinidumpCrashpadInfoWriter() override;

  //! \brief Arranges for MinidumpCrashpadInfo::module_list to point to the
  //!     MinidumpModuleCrashpadInfoList object to be written by \a
  //!     module_list.
  //!
  //! This object takes ownership of \a module_list and becomes its parent in
  //! the overall tree of internal::MinidumpWritable objects.
  //!
  //! \note Valid in #kStateMutable.
  void SetModuleList(
      scoped_ptr<MinidumpModuleCrashpadInfoListWriter> module_list);

 protected:
  // MinidumpWritable:
  bool Freeze() override;
  size_t SizeOfObject() override;
  std::vector<MinidumpWritable*> Children() override;
  bool WriteObject(FileWriterInterface* file_writer) override;

  // MinidumpStreamWriter:
  MinidumpStreamType StreamType() const override;

 private:
  MinidumpCrashpadInfo crashpad_info_;
  scoped_ptr<MinidumpModuleCrashpadInfoListWriter> module_list_;

  DISALLOW_COPY_AND_ASSIGN(MinidumpCrashpadInfoWriter);
};

}  // namespace crashpad

#endif  // CRASHPAD_MINIDUMP_MINIDUMP_CRASHPAD_INFO_WRITER_H_